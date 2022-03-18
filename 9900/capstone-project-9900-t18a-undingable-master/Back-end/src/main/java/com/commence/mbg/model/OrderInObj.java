package com.commence.mbg.model;

import java.util.List;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description:
 * @Date: 2021/11/7 16:04
 * @Auther: Jiahui Wang
 */
public class OrderInObj {

    /**
     * User Id
     */
    private Long userId;

    /**
     * Total price
     */
    private Long amount;

    /**
     * Product list
     */
    private List<ProductInObj> products;

    @Override
    public String toString() {
        return "OrderInObj{" +
                "userId=" + userId +
                ", amount=" + amount +
                ", products=" + products +
                '}';
    }

    public OrderInObj(Long userId, Long amount, List<ProductInObj> products) {
        this.userId = userId;
        this.amount = amount;
        this.products = products;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public Long getAmount() {
        return amount;
    }

    public void setAmount(Long amount) {
        this.amount = amount;
    }

    public List<ProductInObj> getProducts() {
        return products;
    }

    public void setProducts(List<ProductInObj> products) {
        this.products = products;
    }

    public OrderInObj() {
    }
}
