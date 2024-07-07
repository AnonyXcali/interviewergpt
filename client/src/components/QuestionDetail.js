import React from 'react';
import { Card } from 'antd';

const QuestionDetail = ({ question }) => {
  return (
    <Card title={question.description}>
      <p>Company: {question.company}</p>
      <p>Type: {question.type}</p>
      <p>Difficulty: {question.difficulty_score}</p>
      <p>AAS: {question.aas}</p>
      <p>Solution: {question.solution}</p>
    </Card>
  );
};

export default QuestionDetail;
