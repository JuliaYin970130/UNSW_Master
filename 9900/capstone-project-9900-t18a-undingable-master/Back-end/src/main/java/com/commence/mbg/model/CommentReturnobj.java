package com.commence.mbg.model;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description:
 * @Date: 2021/11/7 16:59
 * @Auther: Jiahui Wang
 */
public class CommentReturnobj {

    private User user;

    private String comment;

    private Long productId;

    private Long order_Id;

    private Integer stars;


    @Override
    public String toString() {
        return "CommentReturnobj{" +
                "user=" + user +
                ", comment='" + comment + '\'' +
                ", productId=" + productId +
                ", order_Id=" + order_Id +
                ", stars=" + stars +
                '}';
    }

    public User getUser() {
        return user;
    }

    public Integer getStars() {
        return stars;
    }

    public void setStars(Integer stars) {
        this.stars = stars;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public String getComment() {
        return comment;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }

    public Long getProductId() {
        return productId;
    }

    public void setProductId(Long productId) {
        this.productId = productId;
    }

    public Long getOrder_Id() {
        return order_Id;
    }

    public void setOrder_Id(Long order_Id) {
        this.order_Id = order_Id;
    }
}
