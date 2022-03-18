package com.commence.mbg.model;

import java.util.Date;
import java.util.List;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description: Return obj for Order
 * @Date: 2021/11/7 15:41
 * @Auther: Jiahui Wang
 */
public class OrderReturnObj {

    private Long orderId;

    private Long userId;

    private Date orderTime;

    private Long TotalPrice;

    private List<Orderdetail> orderdetail;

    public OrderReturnObj() {
    }

    public OrderReturnObj(Long orderId, Long userId, Date orderTime, List<Orderdetail> orderdetail) {
        this.orderId = orderId;
        this.userId = userId;
        this.orderTime = orderTime;
        this.orderdetail = orderdetail;
    }

    public Long getOrderId() {
        return orderId;
    }

    public void setOrderId(Long orderId) {
        this.orderId = orderId;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public Date getOrderTime() {
        return orderTime;
    }

    public void setOrderTime(Date orderTime) {
        this.orderTime = orderTime;
    }

    public List<Orderdetail> getOrderdetail() {
        return orderdetail;
    }

    public void setOrderdetail(List<Orderdetail> orderdetail) {
        this.orderdetail = orderdetail;
    }

    @Override
    public String toString() {
        return "OrderReturnObj{" +
                "orderId=" + orderId +
                ", userId=" + userId +
                ", orderTime=" + orderTime +
                ", orderdetail=" + orderdetail +
                '}';
    }

    public Long getTotalPrice() {
        return TotalPrice;
    }

    public void setTotalPrice(Long totalPrice) {
        TotalPrice = totalPrice;
    }
}
