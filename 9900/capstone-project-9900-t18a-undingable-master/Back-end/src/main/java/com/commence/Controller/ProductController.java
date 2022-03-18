package com.commence.Controller;

import com.commence.Service.ProductService;
import com.commence.Utils.ReturnResult;
import com.commence.mbg.model.Product;
import com.commence.mbg.model.User;
import org.apache.logging.log4j.core.config.plugins.validation.constraints.Required;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpServletResponse;

/**
 * @program: capstone-project-9900-t18a-undingable
 * @description: controller for product
 * @author: Jiahui Wang
 * @create: 2021-10-27 17:07
 **/
@CrossOrigin(origins = "*")
@Controller
@RequestMapping("/product")
public class ProductController {

    @Autowired
    private ProductService productService;

    @RequestMapping(value = "view", method = RequestMethod.GET)
    @ResponseBody
    public ReturnResult view(Product product){
        return productService.view(product);
    }

    @RequestMapping(value = "viewByPriceRange", method = RequestMethod.GET)
    @ResponseBody
    public ReturnResult viewByPriceRange(Integer low_price, Integer high_price){
        return productService.viewByPriceRange(low_price, high_price);
    }

    @RequestMapping(value = "recommend", method = RequestMethod.GET)
    @ResponseBody
    public ReturnResult recommend(User user, int top_k){
        return productService.recommend(user, top_k);
    }

    @RequestMapping(value = "Sale", method = RequestMethod.GET)
    @ResponseBody
    public ReturnResult get_all_sale(){
        return productService.get_all_sale();
    }

}
