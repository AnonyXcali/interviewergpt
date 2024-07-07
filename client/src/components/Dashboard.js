import React, { useState, useEffect } from 'react';
import { Input, Select, List, Button } from 'antd';
import axios from 'axios';
import FilterForm from './FilterForm';
import QuestionDetail from './QuestionDetail';

const { Option } = Select;

const Dashboard = () => {
  const [questions, setQuestions] = useState([]);
  const [filteredQuestions, setFilteredQuestions] = useState([]);
  const [selectedQuestion, setSelectedQuestion] = useState(null);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await axios.get('http://<your-server-ip>:5000/questions');
        setQuestions(response.data);
        setFilteredQuestions(response.data);
      } catch (error) {
        console.error('Error fetching questions', error);
      }
    };

    fetchQuestions();
  }, []);

  const handleFilter = (filters) => {
    const filtered = questions.filter((question) => {
      return (
        (!filters.text || question.description.includes(filters.text)) &&
        (!filters.company || question.company === filters.company) &&
        (!filters.difficulty || question.difficulty_score === filters.difficulty) &&
        (!filters.aas || question.aas === filters.aas)
      );
    });
    setFilteredQuestions(filtered);
  };

  return (
    <div>
      <FilterForm onFilter={handleFilter} />
      <List
        itemLayout="horizontal"
        dataSource={filteredQuestions}
        renderItem={(item) => (
          <List.Item>
            <List.Item.Meta
              title={<Button type="link" onClick={() => setSelectedQuestion(item)}>{item.description}</Button>}
              description={`Company: ${item.company}, Type: ${item.type}, Difficulty: ${item.difficulty_score}, AAS: ${item.aas}`}
            />
          </List.Item>
        )}
      />
      {selectedQuestion && <QuestionDetail question={selectedQuestion} />}
    </div>
  );
};

export default Dashboard;
