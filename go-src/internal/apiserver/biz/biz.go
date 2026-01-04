package biz

type IBiz interface{}

type biz struct {
}

var _ IBiz = (*biz)(nil)

func NewBiz() *biz {
	return &biz{}
}
