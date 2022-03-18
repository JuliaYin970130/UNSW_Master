package com.commence.mbg.model;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description:
 * @Date: 2021/11/6 15:42
 * @Auther: Jiahui Wang
 */
public class ShoppingCartObj {

    private static final long serialVersionUID = 1L;

    /**
     * Shopping cart ID
     */
    Long shoppingCartId;

    /**
     * Product obj
     */
    Product product;

    /**
     * Number of product in the shopping cart
     */
    Long quantity;

    public ShoppingCartObj() {
    }

    public ShoppingCartObj(Long shoppingCartId, Product product, Long quantity) {
        this.shoppingCartId = shoppingCartId;
        this.product = product;
        this.quantity = quantity;
    }

    public Long getShoppingCartId() {
        return shoppingCartId;
    }

    public void setShoppingCartId(Long shoppingCartId) {
        this.shoppingCartId = shoppingCartId;
    }

    public Product getProduct() {
        return product;
    }

    public void setProduct(Product product) {
        this.product = product;
    }

    public Long getQuantity() {
        return quantity;
    }

    public void setQuantity(Long quantity) {
        this.quantity = quantity;
    }

    @Override
    public String toString() {
        return "ShoppingCartObj{" +
                "shoppingCartId=" + shoppingCartId +
                ", product=" + product +
                ", quantity=" + quantity +
                '}';
    }
}
