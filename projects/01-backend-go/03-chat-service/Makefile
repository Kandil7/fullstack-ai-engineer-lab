.PHONY: run build test test-race cover vet tidy migrate-up migrate-down docker

DB_URL ?= postgres://fslab:fslab_dev_2026@localhost:5432/fslab?sslmode=disable

run:
	go run ./src/cmd/server

build:
	go build -o bin/chat-service ./src/cmd/server

test:
	go test ./...

test-race:
	go test -race ./...

cover:
	go test -cover ./...

vet:
	go vet ./...

tidy:
	go mod tidy

migrate-up:
	@for f in migrations/*.up.sql; do echo "  -> $$f"; psql "$(DB_URL)" -f $$f; done

migrate-down:
	@for f in $$(ls -r migrations/*.down.sql); do echo "  -> $$f"; psql "$(DB_URL)" -f $$f; done

docker:
	docker build -t fslab/chat-service .
