"""
Ingestion pipeline for code repositories and documents.
"""

import hashlib
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Set

from devmate.config import settings
from devmate.obs.tracing import tracer


@dataclass
class Document:
    """A document chunk with metadata."""
    id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata,
        }


class BaseChunker(ABC):
    """Abstract base class for document chunkers."""
    
    @abstractmethod
    def chunk(self, content: str, metadata: Dict[str, Any]) -> List[Document]:
        """Split content into chunks."""
        pass
    
    def _generate_id(self, content: str, source: str, position: int) -> str:
        """Generate deterministic ID from content hash."""
        hash_input = f"{source}:{position}:{content[:100]}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:16]


class FixedSizeChunker(BaseChunker):
    """Fixed-size chunking with overlap."""
    
    def __init__(
        self,
        chunk_size: int = None,
        overlap: int = None,
    ):
        self.chunk_size = chunk_size or settings.rag_chunk_size
        self.overlap = overlap or settings.rag_chunk_overlap
    
    def chunk(self, content: str, metadata: Dict[str, Any]) -> List[Document]:
        """Chunk text into fixed-size pieces with overlap."""
        source = metadata.get("source", "unknown")
        chunks = []
        
        start = 0
        position = 0
        
        while start < len(content):
            end = min(start + self.chunk_size, len(content))
            
            # Try to break at word boundary
            if end < len(content):
                # Find last space before end
                last_space = content.rfind(' ', start, end)
                if last_space > start:
                    end = last_space
            
            chunk_content = content[start:end].strip()
            
            if chunk_content:
                chunk_metadata = metadata.copy()
                chunk_metadata.update({
                    "chunk_index": position,
                    "chunk_start": start,
                    "chunk_end": end,
                    "chunker": "fixed_size",
                })
                
                doc = Document(
                    id=self._generate_id(chunk_content, source, position),
                    content=chunk_content,
                    metadata=chunk_metadata,
                )
                chunks.append(doc)
                position += 1
            
            start = end - self.overlap
            if start >= len(content):
                break
        
        return chunks


class RecursiveChunker(BaseChunker):
    """Recursive text splitting by separators."""
    
    def __init__(
        self,
        chunk_size: int = None,
        overlap: int = None,
        separators: List[str] = None,
    ):
        self.chunk_size = chunk_size or settings.rag_chunk_size
        self.overlap = overlap or settings.rag_chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]
    
    def chunk(self, content: str, metadata: Dict[str, Any]) -> List[Document]:
        """Recursively split text by separators."""
        source = metadata.get("source", "unknown")
        chunks = self._split_text(content, self.separators)
        
        documents = []
        for i, chunk_content in enumerate(chunks):
            if not chunk_content.strip():
                continue
            
            chunk_metadata = metadata.copy()
            chunk_metadata.update({
                "chunk_index": i,
                "chunker": "recursive",
            })
            
            doc = Document(
                id=self._generate_id(chunk_content, source, i),
                content=chunk_content.strip(),
                metadata=chunk_metadata,
            )
            documents.append(doc)
        
        return documents
    
    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        """Recursively split text."""
        if not separators:
            return [text[i:i + self.chunk_size] for i in range(0, len(text), self.chunk_size)]
        
        separator = separators[0]
        remaining_separators = separators[1:]
        
        if separator == "":
            # Character-level split
            return [text[i:i + self.chunk_size] for i in range(0, len(text), self.chunk_size)]
        
        splits = text.split(separator)
        
        # If no splits happened or all splits are small enough, return as-is
        if len(splits) == 1 or all(len(s) <= self.chunk_size for s in splits):
            if remaining_separators:
                return self._split_text(text, remaining_separators)
            return splits
        
        # Recursively split large chunks
        result = []
        for split in splits:
            if len(split) <= self.chunk_size:
                result.append(split)
            else:
                result.extend(self._split_text(split, remaining_separators))
        
        return result


class ASTAwareChunker(BaseChunker):
    """AST-aware chunking for source code."""
    
    def __init__(
        self,
        chunk_size: int = None,
        overlap: int = None,
    ):
        self.chunk_size = chunk_size or settings.rag_chunk_size
        self.overlap = overlap or settings.rag_chunk_overlap
    
    def chunk(self, content: str, metadata: Dict[str, Any]) -> List[Document]:
        """Chunk code by AST boundaries (functions, classes)."""
        source = metadata.get("source", "unknown")
        language = metadata.get("language", "").lower()
        
        # Simple heuristic-based code chunking
        # In production, use tree-sitter or language-specific parsers
        if language in ("python", "py"):
            return self._chunk_python(content, metadata)
        elif language in ("javascript", "typescript", "js", "ts"):
            return self._chunk_js_ts(content, metadata)
        else:
            # Fallback to recursive chunking
            fallback = RecursiveChunker(self.chunk_size, self.overlap)
            return fallback.chunk(content, metadata)
    
    def _chunk_python(self, content: str, metadata: Dict[str, Any]) -> List[Document]:
        """Chunk Python code by functions and classes."""
        import ast
        
        source = metadata.get("source", "unknown")
        chunks = []
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            # Fallback for invalid syntax
            fallback = RecursiveChunker(self.chunk_size, self.overlap)
            return fallback.chunk(content, metadata)
        
        # Extract top-level functions and classes
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                # Get the source code for this node
                start_line = node.lineno - 1
                end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 50
                
                lines = content.split('\n')
                chunk_lines = lines[start_line:end_line]
                chunk_content = '\n'.join(chunk_lines)
                
                if len(chunk_content) > self.chunk_size * 4:
                    # Too large, split further
                    continue
                
                chunk_metadata = metadata.copy()
                chunk_metadata.update({
                    "chunk_type": "function" if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else "class",
                    "name": node.name,
                    "start_line": start_line + 1,
                    "end_line": end_line,
                    "chunker": "ast_aware",
                })
                
                doc = Document(
                    id=self._generate_id(chunk_content, source, len(chunks)),
                    content=chunk_content,
                    metadata=chunk_metadata,
                )
                chunks.append(doc)
        
        # If no AST chunks found, fallback
        if not chunks:
            fallback = RecursiveChunker(self.chunk_size, self.overlap)
            return fallback.chunk(content, metadata)
        
        return chunks
    
    def _chunk_js_ts(self, content: str, metadata: Dict[str, Any]) -> List[Document]:
        """Chunk JavaScript/TypeScript code by functions and classes."""
        # Simple regex-based approach for JS/TS
        import re
        
        source = metadata.get("source", "unknown")
        chunks = []
        
        # Match function declarations, arrow functions, class declarations
        patterns = [
            r'(export\s+)?(async\s+)?function\s+\w+\s*\([^)]*\)\s*\{',
            r'(export\s+)?const\s+\w+\s*=\s*(async\s+)?\([^)]*\)\s*=>\s*\{',
            r'(export\s+)?class\s+\w+\s*\{',
        ]
        
        # Find all matches with positions
        matches = []
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                matches.append((match.start(), match.group()))
        
        matches.sort(key=lambda x: x[0])
        
        for i, (start_pos, match_text) in enumerate(matches):
            # Find the matching closing brace
            chunk_content = self._extract_balanced_block(content, start_pos)
            
            if len(chunk_content) > self.chunk_size * 4:
                continue
            
            # Extract name from match
            name_match = re.search(r'(function|const|class)\s+(\w+)', match_text)
            name = name_match.group(2) if name_match else f"block_{i}"
            kind = "function" if "function" in match_text or "=>" in match_text else "class"
            
            chunk_metadata = metadata.copy()
            chunk_metadata.update({
                "chunk_type": kind,
                "name": name,
                "chunker": "ast_aware",
            })
            
            doc = Document(
                id=self._generate_id(chunk_content, source, i),
                content=chunk_content,
                metadata=chunk_metadata,
            )
            chunks.append(doc)
        
        if not chunks:
            fallback = RecursiveChunker(self.chunk_size, self.overlap)
            return fallback.chunk(content, metadata)
        
        return chunks
    
    def _extract_balanced_block(self, content: str, start: int) -> str:
        """Extract a balanced brace block from start position."""
        brace_count = 0
        in_string = False
        string_char = None
        escaped = False
        
        for i in range(start, len(content)):
            char = content[i]
            
            if escaped:
                escaped = False
                continue
            
            if char == '\\':
                escaped = True
                continue
            
            if not in_string and char in ('"', "'", '`'):
                in_string = True
                string_char = char
            elif in_string and char == string_char:
                in_string = False
                string_char = None
            elif not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        return content[start:i+1]
        
        # If we didn't find balanced braces, return reasonable chunk
        return content[start:start + self.chunk_size]


class DocumentLoader:
    """Load documents from various sources."""
    
    SUPPORTED_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.cpp', '.c', '.h',
        '.md', '.txt', '.rst', '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg',
        '.html', '.css', '.scss', '.sql', '.sh', '.bash', '.ps1', '.dockerfile',
    }
    
    def __init__(self, chunker: BaseChunker = None):
        self.chunker = chunker or FixedSizeChunker()
    
    def load_file(self, file_path: Path, metadata: Dict[str, Any] = None) -> List[Document]:
        """Load a single file."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            return []
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            # Skip binary files
            return []
        
        if not content.strip():
            return []
        
        file_metadata = metadata or {}
        file_metadata.update({
            "source": str(file_path),
            "filename": file_path.name,
            "extension": file_path.suffix,
            "size_bytes": file_path.stat().st_size,
        })
        
        return self.chunker.chunk(content, file_metadata)
    
    def load_directory(
        self,
        dir_path: Path,
        recursive: bool = True,
        exclude_patterns: List[str] = None,
        metadata: Dict[str, Any] = None,
    ) -> Iterator[Document]:
        """Load all supported files from a directory."""
        exclude_patterns = exclude_patterns or [
            '__pycache__', '.git', 'node_modules', '.venv', 'venv',
            'dist', 'build', '.next', '.cache', 'target',
        ]
        
        pattern = "**/*" if recursive else "*"
        
        for file_path in dir_path.glob(pattern):
            if not file_path.is_file():
                continue
            
            # Check exclude patterns
            if any(excl in str(file_path) for excl in exclude_patterns):
                continue
            
            try:
                docs = self.load_file(file_path, metadata)
                for doc in docs:
                    yield doc
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    
    def load_repository(
        self,
        repo_path: Path,
        metadata: Dict[str, Any] = None,
    ) -> Iterator[Document]:
        """Load an entire repository."""
        repo_metadata = metadata or {}
        repo_metadata.update({
            "repo_name": repo_path.name,
            "repo_path": str(repo_path),
        })
        
        yield from self.load_directory(repo_path, metadata=repo_metadata)


# Chunker registry
CHUNKERS = {
    "fixed": FixedSizeChunker,
    "recursive": RecursiveChunker,
    "ast_aware": ASTAwareChunker,
}


def get_chunker(name: str, **kwargs) -> BaseChunker:
    """Get chunker by name."""
    if name not in CHUNKERS:
        raise ValueError(f"Unknown chunker: {name}. Available: {list(CHUNKERS.keys())}")
    return CHUNKERS[name](**kwargs)