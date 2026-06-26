# Auth Service — Notes

> Personal notes, learnings, and reflections. Updated as you build.

## What I Built

<!-- Document what you implemented each day -->

### Day 1: Project Scaffold
- 

### Day 2: Database Layer
- 

### Day 3: Service & JWT
- 

### Day 4: HTTP Handlers
- 

### Day 5: Testing & Polish
- 

## What I Learned

<!-- Capture key insights, "aha!" moments, and useful patterns -->

### Go Patterns
- 

### Database Tips
- 

### Auth/JWT Insights
- 

### Testing Strategies
- 

## Issues Encountered

<!-- Log problems and how you solved them for future reference -->

| Date | Issue | Solution | Prevention |
|------|-------|----------|------------|
| | | | |
| | | | |
| | | | |

## Decisions Log

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| Used chi over Gin | More stdlib-aligned | Gin, Echo, Fiber |
| bcrypt cost 12 | Balance security/performance | cost 10 (faster), cost 14 (more secure) |
| RS256 for JWTs | Asymmetric, allows public verification | HS256 (simpler but symmetric) |

## Resources & Links

- [Go chi documentation](https://github.com/go-chi/chi)
- [pgx documentation](https://pkg.go.dev/github.com/jackc/pgx)
- [JWT Go library](https://github.com/golang-jwt/jwt)

---

*Update this file daily. Future-you will thank present-you.*
