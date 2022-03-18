package com.commence.mbg.model;

import io.swagger.annotations.ApiModelProperty;
import java.io.Serializable;

public class Sale implements Serializable {
    private Long saleid;

    private Long productid;

    private Long salenum;

    private static final long serialVersionUID = 1L;

    public Long getSaleid() {
        return saleid;
    }

    public void setSaleid(Long saleid) {
        this.saleid = saleid;
    }

    public Long getProductid() {
        return productid;
    }

    public void setProductid(Long productid) {
        this.productid = productid;
    }

    public Long getSalenum() {
        return salenum;
    }

    public void setSalenum(Long salenum) {
        this.salenum = salenum;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(getClass().getSimpleName());
        sb.append(" [");
        sb.append("Hash = ").append(hashCode());
        sb.append(", saleid=").append(saleid);
        sb.append(", productid=").append(productid);
        sb.append(", salenum=").append(salenum);
        sb.append(", serialVersionUID=").append(serialVersionUID);
        sb.append("]");
        return sb.toString();
    }
}