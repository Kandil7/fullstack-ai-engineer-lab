package user

import (
	"errors"
	"strings"
)

// UpdateProfileRequest is the payload for PUT /users/:id.
type UpdateProfileRequest struct {
	Name   string `json:"name"`
	Avatar string `json:"avatar"`
	Bio    string `json:"bio"`
}

// Validate checks the update payload for basic correctness.
func (r UpdateProfileRequest) Validate() error {
	name := strings.TrimSpace(r.Name)
	if name == "" {
		return errors.New("name is required")
	}
	if len(name) > 255 {
		return errors.New("name must be 255 characters or fewer")
	}
	if len(r.Bio) > 2000 {
		return errors.New("bio must be 2000 characters or fewer")
	}
	if len(r.Avatar) > 500 {
		return errors.New("avatar url must be 500 characters or fewer")
	}
	return nil
}

// Pagination describes a page cursor and total for list responses.
type Pagination struct {
	Cursor  string `json:"cursor,omitempty"`
	HasMore bool   `json:"has_more"`
	Total   int    `json:"total"`
}

// ListResponse is the envelope for GET /users.
type ListResponse struct {
	Data       []User     `json:"data"`
	Pagination Pagination `json:"pagination"`
}

// ErrorResponse is the standard error envelope.
type ErrorResponse struct {
	Error string `json:"error"`
}
