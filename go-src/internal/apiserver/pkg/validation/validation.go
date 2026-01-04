package validation

import (
	"github.com/pachirode/ffmpeg-study/internal/pkg/errno"
	"regexp"
)

type Validator struct {
	// 有些复杂的验证逻辑，可能需要直接查询数据库
	//store store.IStore
}

// 使用预编译的全局正则表达式，避免重复创建和编译.
var (
	lengthRegex = regexp.MustCompile(`^.{3,20}$`)                                        // 长度在 3 到 20 个字符之间
	validRegex  = regexp.MustCompile(`^[A-Za-z0-9_]+$`)                                  // 仅包含字母、数字和下划线
	letterRegex = regexp.MustCompile(`[A-Za-z]`)                                         // 至少包含一个字母
	numberRegex = regexp.MustCompile(`\d`)                                               // 至少包含一个数字
	emailRegex  = regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`) // 邮箱格式
	phoneRegex  = regexp.MustCompile(`^1[3-9]\d{9}$`)                                    // 中国手机号
)

// New 创建一个新的 Validator 实例.
func New() *Validator {
	return &Validator{}
}

// isValidUsername 校验用户名是否合法.
func isValidUsername(username string) bool {
	// 校验长度
	if !lengthRegex.MatchString(username) {
		return false
	}
	// 校验字符合法性
	if !validRegex.MatchString(username) {
		return false
	}
	return true
}

// isValidPassword 判断密码是否符合复杂度要求.
func isValidPassword(password string) error {
	switch {
	// 检查新密码是否为空
	case password == "":
		return errno.ErrInvalidArgument.WithMessage("password cannot be empty")
	// 检查新密码的长度要求
	case len(password) < 6:
		return errno.ErrInvalidArgument.WithMessage("password must be at least 6 characters long")
	// 使用正则表达式检查是否至少包含一个字母
	case !letterRegex.MatchString(password):
		return errno.ErrInvalidArgument.WithMessage("password must contain at least one letter")
	// 使用正则表达式检查是否至少包含一个数字
	case !numberRegex.MatchString(password):
		return errno.ErrInvalidArgument.WithMessage("password must contain at least one number")
	}
	return nil
}

// isValidEmail 判断电子邮件是否合法.
func isValidEmail(email string) error {
	// 检查电子邮件地址格式
	if email == "" {
		return errno.ErrInvalidArgument.WithMessage("email cannot be empty")
	}

	// 使用正则表达式校验电子邮件格式
	if !emailRegex.MatchString(email) {
		return errno.ErrInvalidArgument.WithMessage("invalid email format")
	}

	return nil
}
