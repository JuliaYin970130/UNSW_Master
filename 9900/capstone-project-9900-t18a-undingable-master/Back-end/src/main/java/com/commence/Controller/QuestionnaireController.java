package com.commence.Controller;

import com.commence.Service.QuestionaireService;
import com.commence.Utils.ReturnResult;
import com.commence.mbg.model.Questionaire;
import com.commence.mbg.model.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpServletResponse;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description: Controller for questionaire
 * @Date: 2021/11/4 16:49
 * @Auther: Jiahui Wang
 */
@CrossOrigin(origins = "*")
@Controller
@RequestMapping("/questionnaire")
public class QuestionnaireController {

    @Autowired
    private QuestionaireService questionaireService;

    @RequestMapping(value = "get", method = RequestMethod.GET)
    @ResponseBody
    public ReturnResult get_questionnaire(Questionaire questionaire){
        return questionaireService.get_questionnaire(questionaire);
    }

    @RequestMapping(value = "insert", method = RequestMethod.POST)
    @ResponseBody
    public ReturnResult insert_questionnaire(Questionaire questionaire){
        return questionaireService.insert_questionnaire(questionaire);
    }

    @RequestMapping(value = "update", method = RequestMethod.POST)
    @ResponseBody
    public ReturnResult update_questionnaire(Questionaire questionaire){
        return questionaireService.update_questionnaire(questionaire);
    }

}
