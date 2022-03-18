package com.commence.Service.Impl;

import com.commence.Service.ProductService;
import com.commence.Utils.ReturnResult;
import com.commence.mbg.mapper.ProductDaoMapper;
import com.commence.mbg.mapper.ProductMapper;
import com.commence.mbg.mapper.QuestionaireMapper;
import com.commence.mbg.mapper.SaleMapper;
import com.commence.mbg.mapper.UserMapper;
import com.commence.mbg.model.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import java.util.*;

/**
 * @program: capstone-project-9900-t18a-undingable
 * @description: Product service implementation
 * @author: Jiahui Wang
 * @create: 2021-10-27 17:08
 **/
@Service
public class ProductServiceImpl implements ProductService {

    @Autowired
    private UserMapper userMapper;

    @Autowired
    private ProductMapper productMapper;

    @Autowired
    private ProductDaoMapper productDaoMapper;

    @Autowired
    private QuestionaireMapper questionaireMapper;

    @Autowired
    private SaleMapper saleMapper;

    @Override
    public ReturnResult view(Product product) {
        ProductExample example = new ProductExample();
        Boolean return_all = true;

        if (product.getId() != null){
            example.createCriteria().andIdEqualTo(product.getId());
            return_all = false;
        }
        if (product.getName() != null){
            example.createCriteria().andNameLike("%" + product.getName() + "%");
            return_all = false;
        }
        if (product.getBrand() != null){
            example.createCriteria().andBrandEqualTo(product.getBrand());
            return_all = false;
        }
        if (product.getGender() != null){
            example.createCriteria().andGenderEqualTo(product.getGender());
            return_all = false;
        }
        if (product.getScentNotes() != null){
            example.createCriteria().andScentNotesEqualTo(product.getScentNotes());
            return_all = false;
        }
        if (product.getPrice() != null){
            example.createCriteria().andPriceEqualTo(product.getPrice());
            return_all = false;
        }
        List <Product> productList;
        if (return_all) {
            productList = productDaoMapper.findAll();
        } else {
            productList = productMapper.selectByExample(example);
        }
        return ReturnResult.success(productList, "Return successfully");
    }

    @Override
    public ReturnResult viewByPriceRange(Integer low_price, Integer high_price) {
        if (low_price == null || high_price == null){
            return ReturnResult.failed(503, null, "low_price or high_price is null, please check");
        }
        List<Product> productList= productDaoMapper.findProductByPriceRange(low_price, high_price);
        return ReturnResult.success(productList, "Find" + low_price + " To " + high_price + " Success!");
    }

    @Override
    public ReturnResult recommend(User user, int top_k) {
        List<Sale> top_sale = top_sale();
        List<Product> top_product = new ArrayList<>();
        int product_num = top_k;
        for (Sale sale: top_sale){
            if (product_num -- > 0) {
                top_product.add(productMapper.selectByPrimaryKey(sale.getProductid()));
            } else {
                break;
            }
        }
        if (user.getId() == null){
            // then return top sale
            return ReturnResult.success(top_product, "return Top-k sale product successfully");
        } else {
            QuestionaireExample example = new QuestionaireExample();
            example.createCriteria().andUseridEqualTo(user.getId());
            List<Questionaire> questionnaireList = questionaireMapper.selectByExample(example);
            if (questionnaireList.size() == 0) {
                // then return top sale
                return ReturnResult.success(top_product, "return Top-k sale product successfully(not filled in questionnaire)");
            }
            // Obtain all products
            ProductExample productExample = new ProductExample();
            List<Product> all_product = productMapper.selectByExample(productExample);

            Questionaire questionaire = questionnaireList.get(0);
            Map<Double, Product> weights = new TreeMap<>(Comparator.reverseOrder());
            for (Product product : all_product) {
                SaleExample saleExample = new SaleExample();
                saleExample.createCriteria().andProductidEqualTo(product.getId());

                List<Sale> saleList = saleMapper.selectByExample(saleExample);
                double weight = 2;
                if (saleList.size() != 0){
                    weight = saleList.get(0).getSalenum();
                    // 削弱初始 weight 的影响
                    weight /= 5000;
                    weight = weight < 1 ? 1 + weight : weight;
                }

                // Compare brand
                if (product.getBrand().equalsIgnoreCase(questionaire.getBrand())) {
                    weight *= 1.6;
                } else {
                    weight *= 1.2;
                }
                // Compare Family
                if (product.getScentNotes().equalsIgnoreCase(questionaire.getFamily())) {
                    weight *= 4.0;
                } else {
                    weight *= 1.3;
                }
                // Compare brand
                Map<String, String> gender_map = new HashMap<>();
                gender_map.put("her", "Women");
                gender_map.put("him", "Men");
                if (product.getGender().equalsIgnoreCase(gender_map.get(questionaire.getForwho()))) {
                    weight *= 3.0;
                } else {
                    weight *= 1.1;
                }
                if (product.getGender().equalsIgnoreCase("Unisex")){
                    weight *= 1.5;
                }
                // Compare brand
                if (product.getPrice() > questionaire.getLowerprice() && product.getPrice() < questionaire.getHigherprice()) {
                    weight *= 1.7;
                } else {
                    weight *= 1.1;
                }
                weights.put(weight, product);
            }
            top_product = new ArrayList<>();
            product_num = top_k;
            for (Product product: weights.values()){
                if (product_num -- > 0) {
                    top_product.add(product);
                } else {
                    break;
                }
            }
            return ReturnResult.success(top_product, "return Top-k sale product successfully(filled in questionnaire)");
        }
    }

    @Override
    public ReturnResult get_all_sale() {
        SaleExample example = new SaleExample();
        List<Sale> sale = saleMapper.selectByExample(example);
        return ReturnResult.success(sale, "return sale successfully");
    }

    public List<Sale> top_sale(){
        SaleExample example = new SaleExample();
        example.setOrderByClause("SaleNum DESC");
        return saleMapper.selectByExample(example);
    }



}
