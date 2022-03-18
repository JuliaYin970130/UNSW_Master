package com.commence.mbg.model;

import io.swagger.annotations.ApiModelProperty;
import java.io.Serializable;

public class Questionaire implements Serializable {
    private Long questionireid;

    private Long userid;

    private String family;

    private String forwho;

    private Long lowerprice;

    private Long higherprice;

    private String brand;

    private static final long serialVersionUID = 1L;

    public Long getQuestionireid() {
        return questionireid;
    }

    public void setQuestionireid(Long questionireid) {
        this.questionireid = questionireid;
    }

    public Long getUserid() {
        return userid;
    }

    public void setUserid(Long userid) {
        this.userid = userid;
    }

    public String getFamily() {
        return family;
    }

    public void setFamily(String family) {
        this.family = family;
    }

    public String getForwho() {
        return forwho;
    }

    public void setForwho(String forwho) {
        this.forwho = forwho;
    }

    public Long getLowerprice() {
        return lowerprice;
    }

    public void setLowerprice(Long lowerprice) {
        this.lowerprice = lowerprice;
    }

    public Long getHigherprice() {
        return higherprice;
    }

    public void setHigherprice(Long higherprice) {
        this.higherprice = higherprice;
    }

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
        this.brand = brand;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(getClass().getSimpleName());
        sb.append(" [");
        sb.append("Hash = ").append(hashCode());
        sb.append(", questionireid=").append(questionireid);
        sb.append(", userid=").append(userid);
        sb.append(", family=").append(family);
        sb.append(", forwho=").append(forwho);
        sb.append(", lowerprice=").append(lowerprice);
        sb.append(", higherprice=").append(higherprice);
        sb.append(", brand=").append(brand);
        sb.append(", serialVersionUID=").append(serialVersionUID);
        sb.append("]");
        return sb.toString();
    }
}