"""
Tracing and observability with Langfuse integration.
"""

import os
import uuid
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional, Generator, AsyncGenerator

from devmate.config import settings


@dataclass
class Span:
    """A single trace span."""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: list = field(default_factory=list)
    status: str = "ok"
    error: Optional[str] = None
    
    def set_attribute(self, key: str, value: Any):
        """Set a span attribute."""
        self.attributes[key] = value
    
    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        """Add an event to the span."""
        self.events.append({
            "name": name,
            "timestamp": datetime.utcnow().isoformat(),
            "attributes": attributes or {},
        })
    
    def set_status(self, status: str, error: Optional[str] = None):
        """Set span status."""
        self.status = status
        if error:
            self.error = error
            self.attributes["error"] = error
    
    def finish(self):
        """Mark span as finished."""
        self.end_time = datetime.utcnow()
    
    def duration_ms(self) -> float:
        """Get span duration in milliseconds."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "name": self.name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": self.duration_ms(),
            "attributes": self.attributes,
            "events": self.events,
            "status": self.status,
            "error": self.error,
        }


@dataclass
class Trace:
    """A complete trace with multiple spans."""
    trace_id: str
    name: str
    start_time: datetime
    spans: Dict[str, Span] = field(default_factory=dict)
    root_span_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_span(self, span: Span):
        """Add a span to the trace."""
        self.spans[span.span_id] = span
        if self.root_span_id is None:
            self.root_span_id = span.span_id
    
    def get_span(self, span_id: str) -> Optional[Span]:
        """Get a span by ID."""
        return self.spans.get(span_id)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "name": self.name,
            "start_time": self.start_time.isoformat(),
            "spans": {sid: span.to_dict() for sid, span in self.spans.items()},
            "root_span_id": self.root_span_id,
            "metadata": self.metadata,
        }


class Tracer:
    """Tracing system with optional Langfuse export."""
    
    def __init__(self):
        self.enabled = settings.tracing_enabled
        self._traces: Dict[str, Trace] = {}
        self._current_trace_id: Optional[str] = None
        self._current_span_id: Optional[str] = None
        self._langfuse_client = None
        self._init_langfuse()
    
    def _init_langfuse(self):
        """Initialize Langfuse client if configured."""
        if not self.enabled:
            return
        
        public_key = settings.langfuse_public_key
        secret_key = settings.langfuse_secret_key
        
        if public_key and secret_key:
            try:
                from langfuse import Langfuse
                self._langfuse_client = Langfuse(
                    public_key=public_key,
                    secret_key=secret_key,
                    host=settings.langfuse_host,
                )
                print(f"Langfuse initialized: {settings.langfuse_host}")
            except ImportError:
                print("Langfuse not installed. Run: pip install langfuse")
            except Exception as e:
                print(f"Failed to initialize Langfuse: {e}")
        else:
            print("Langfuse keys not configured. Tracing will be local only.")
    
    def start_trace(self, name: str, metadata: Optional[Dict[str, Any]] = None) -> Trace:
        """Start a new trace."""
        trace_id = str(uuid.uuid4())
        trace = Trace(
            trace_id=trace_id,
            name=name,
            start_time=datetime.utcnow(),
            metadata=metadata or {},
        )
        self._traces[trace_id] = trace
        self._current_trace_id = trace_id
        return trace
    
    def get_current_trace(self) -> Optional[Trace]:
        """Get the currently active trace."""
        if self._current_trace_id:
            return self._traces.get(self._current_trace_id)
        return None
    
    @contextmanager
    def trace(self, name: str, **attributes) -> Generator[Span, None, None]:
        """Context manager for synchronous tracing."""
        span = self.start_span(name, **attributes)
        try:
            yield span
            span.set_status("ok")
        except Exception as e:
            span.set_status("error", str(e))
            raise
        finally:
            self.end_span(span)
    
    @asynccontextmanager
    async def trace_async(self, name: str, **attributes) -> AsyncGenerator[Span, None]:
        """Async context manager for tracing."""
        span = self.start_span(name, **attributes)
        try:
            yield span
            span.set_status("ok")
        except Exception as e:
            span.set_status("error", str(e))
            raise
        finally:
            self.end_span(span)
    
    def start_span(
        self,
        name: str,
        parent_span_id: Optional[str] = None,
        **attributes,
    ) -> Span:
        """Start a new span."""
        trace_id = self._current_trace_id or str(uuid.uuid4())
        span_id = str(uuid.uuid4())[:16]
        
        parent = parent_span_id or self._current_span_id
        
        span = Span(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent,
            name=name,
            start_time=datetime.utcnow(),
            attributes=attributes,
        )
        
        # Get or create trace
        if trace_id not in self._traces:
            self._traces[trace_id] = Trace(
                trace_id=trace_id,
                name=name,
                start_time=datetime.utcnow(),
            )
        
        self._traces[trace_id].add_span(span)
        self._current_span_id = span_id
        
        return span
    
    def end_span(self, span: Span):
        """End a span."""
        span.finish()
        self._current_span_id = span.parent_span_id
        
        # Export to Langfuse if available
        if self._langfuse_client:
            self._export_span_to_langfuse(span)
    
    def _export_span_to_langfuse(self, span: Span):
        """Export span to Langfuse."""
        try:
            trace = self._traces.get(span.trace_id)
            if not trace:
                return
            
            langfuse_trace = self._langfuse_client.trace(
                id=span.trace_id,
                name=trace.name,
                metadata=trace.metadata,
            )
            
            langfuse_span = langfuse_trace.span(
                id=span.span_id,
                name=span.name,
                parent_span_id=span.parent_span_id,
                start_time=span.start_time,
                end_time=span.end_time,
                metadata=span.attributes,
                level="ERROR" if span.status == "error" else "DEFAULT",
                status_message=span.error,
            )
            
            self._langfuse_client.flush()
        except Exception as e:
            print(f"Failed to export to Langfuse: {e}")
    
    def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Get a trace by ID."""
        return self._traces.get(trace_id)
    
    def get_recent_traces(self, limit: int = 100) -> list:
        """Get recent traces."""
        return list(self._traces.values())[-limit:]
    
    def clear(self):
        """Clear all traces (for testing)."""
        self._traces.clear()
        self._current_trace_id = None
        self._current_span_id = None


# Global tracer instance
tracer = Tracer()


# Convenience decorators
def traced(name: Optional[str] = None, **attributes):
    """Decorator to trace a function."""
    def decorator(func):
        trace_name = name or f"{func.__module__}.{func.__qualname__}"
        
        if asyncio.iscoroutinefunction(func):
            async def async_wrapper(*args, **kwargs):
                async with tracer.trace_async(trace_name, **attributes) as span:
                    span.set_attribute("function", func.__qualname__)
                    return await func(*args, **kwargs)
            return async_wrapper
        else:
            def sync_wrapper(*args, **kwargs):
                with tracer.trace(trace_name, **attributes) as span:
                    span.set_attribute("function", func.__qualname__)
                    return func(*args, **kwargs)
            return sync_wrapper
    
    return decorator


import asyncio