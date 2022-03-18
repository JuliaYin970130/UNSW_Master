package com.commence.mbg.model;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description:
 * @Date: 2021/11/7 16:06
 * @Auther: Jiahui Wang
 */
public class ProductInObj {

    private Long product_id;

    private Long price;

    private Long quantity;

    public ProductInObj(Long product_id, Long price, Long quantity) {
        this.product_id = product_id;
        this.price = price;
        this.quantity = quantity;
    }

    public ProductInObj() {
    }

    @Override
    public String toString() {
        return "ProductInObj{" +
                "product_id=" + product_id +
                ", price=" + price +
                ", quantity=" + quantity +
                '}';
    }

    public Long getProduct_id() {
        return product_id;
    }

    public void setProduct_id(Long product_id) {
        this.product_id = product_id;
    }

    public Long getPrice() {
        return price;
    }

    public void setPrice(Long price) {
        this.price = price;
    }

    public Long getQuantity() {
        return quantity;
    }

    public void setQuantity(Long quantity) {
        this.quantity = quantity;
    }
}
