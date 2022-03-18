package com.commence.Service.Impl;

import com.commence.Service.QuestionaireService;
import com.commence.Utils.ReturnResult;
import com.commence.mbg.mapper.QuestionaireMapper;
import com.commence.mbg.model.Questionaire;
import com.commence.mbg.model.QuestionaireExample;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description:
 * @Date: 2021/11/4 16:51
 * @Auther: Jiahui Wang
 */
@Service
public class QuestionaireServiceImpl implements QuestionaireService {

    @Autowired
    private QuestionaireMapper questionaireMapper;

    @Override
    public ReturnResult get_questionnaire(Questionaire questionaire) {
        Long userId = questionaire.getUserid();
        if (userId == null){
            return ReturnResult.failed(502, null, "UserId is missing, please check");
        }
        QuestionaireExample example = new QuestionaireExample();
        example.createCriteria().andUseridEqualTo(userId);
        List<Questionaire> resque = questionaireMapper.selectByExample(example);

        if (resque.size() == 1) {
            return ReturnResult.success(resque, "Get questionnaire successfully!");
        } else if (resque.size() < 1){
            return ReturnResult.failed(503, null, "This user has not filled the questionnaire!");
        }
        return ReturnResult.failed(504, null, "Something bad occurs, please check with Gary!");
    }

    @Override
    public ReturnResult insert_questionnaire(Questionaire questionaire) {
        QuestionaireExample example = new QuestionaireExample();
        example.createCriteria().andUseridEqualTo(questionaire.getUserid());
        List<Questionaire> resque = questionaireMapper.selectByExample(example);
        if (resque.size() == 1) {
            return ReturnResult.failed(501, null, "This user has already have filled in questionnaire!");
        }

        if (questionaire.getUserid() == null){
            return ReturnResult.failed(502, null, "UserId is missing, please check");
        } else if (questionaire.getFamily() == null){
            return ReturnResult.failed(502, null, "Family is missing, please check");
        } else if (questionaire.getForwho() == null){
            return ReturnResult.failed(502, null, "For who is missing, please check");
        } else if (questionaire.getHigherprice() == null){
            return ReturnResult.failed(502, null, "High price is missing, please check");
        } else if (questionaire.getLowerprice() == null){
            return ReturnResult.failed(502, null, "Low price is missing, please check");
        }
        if (questionaireMapper.insert(questionaire) == 1){
            return ReturnResult.success(questionaire, "Insert questionnaire successfully!");
        } else {
            return ReturnResult.failed(503, null, "Insert questionnaire failed!");
        }
    }

    @Override
    public ReturnResult update_questionnaire(Questionaire questionaire) {
        QuestionaireExample example = new QuestionaireExample();
        example.createCriteria().andUseridEqualTo(questionaire.getUserid());
        Long questionnaire_id = questionaireMapper.selectByExample(example).get(0).getQuestionireid();
        questionaire.setQuestionireid(questionnaire_id);

        if (questionaireMapper.updateByPrimaryKey(questionaire) == 1){
            return ReturnResult.success(questionaire, "Update questionnaire successfully!");
        } else {
            return ReturnResult.failed(503, null, "Update questionnaire failed!");
        }
    }

}
