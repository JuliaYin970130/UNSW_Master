package com.commence.mbg.mapper;

import com.commence.mbg.model.Questionaire;
import com.commence.mbg.model.QuestionaireExample;
import java.util.List;
import org.apache.ibatis.annotations.Param;

public interface QuestionaireMapper {
    int countByExample(QuestionaireExample example);

    int deleteByExample(QuestionaireExample example);

    int deleteByPrimaryKey(Long questionireid);

    int insert(Questionaire record);

    int insertSelective(Questionaire record);

    List<Questionaire> selectByExample(QuestionaireExample example);

    Questionaire selectByPrimaryKey(Long questionireid);

    int updateByExampleSelective(@Param("record") Questionaire record, @Param("example") QuestionaireExample example);

    int updateByExample(@Param("record") Questionaire record, @Param("example") QuestionaireExample example);

    int updateByPrimaryKeySelective(Questionaire record);

    int updateByPrimaryKey(Questionaire record);
}