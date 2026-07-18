// Package user contains the domain model and business logic for user management.
package user

import "time"

// User is the domain representation of a platform user.
type User struct {
	ID        string     `json:"id"`
	Email     string     `json:"email"`
	Name      string     `json:"name"`
	Avatar    string     `json:"avatar,omitempty"`
	Bio       string     `json:"bio,omitempty"`
	Role      string     `json:"role"`
	IsActive  bool       `json:"is_active"`
	DeletedAt *time.Time `json:"-"`
	CreatedAt time.Time  `json:"created_at"`
	UpdatedAt time.Time  `json:"updated_at"`
}

// Stats aggregates a user's learning activity.
type Stats struct {
	UserID           string `json:"user_id"`
	CoursesCompleted int    `json:"courses_completed"`
	QuizzesTaken     int    `json:"quizzes_taken"`
	MessagesSent     int    `json:"messages_sent"`
}

// Valid roles for a user account.
const (
	RoleStudent = "student"
	RoleTeacher = "teacher"
	RoleAdmin   = "admin"
)

// IsValidRole reports whether the given role is recognized.
func IsValidRole(role string) bool {
	switch role {
	case RoleStudent, RoleTeacher, RoleAdmin:
		return true
	default:
		return false
	}
}
