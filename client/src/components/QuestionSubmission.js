import React, { useState } from 'react';
import { Form, Input, Button, Select, InputNumber } from 'antd';
import axios from 'axios';
import CodeEditor from './CodeEditor';

const { Option } = Select;

const QuestionSubmission = () => {
  const [form] = Form.useForm();
  const [code, setCode] = useState('');

  const onFinish = async (values) => {
    try {
      await axios.post('http://34.132.153.144:5000/add-question', {
        ...values,
        custom_solution: code,
      });
      form.resetFields();
      setCode('');
    } catch (error) {
      console.error('Error submitting question', error);
    }
  };

  return (
    <Form form={form} layout="vertical" onFinish={onFinish}>
      <Form.Item name="company" label="Company" rules={[{ required: true }]}>
        <Input />
      </Form.Item>
      <Form.Item name="type" label="Type" rules={[{ required: true }]}>
        <Input />
      </Form.Item>
      <Form.Item name="description" label="Description" rules={[{ required: true }]}>
        <Input.TextArea rows={4} />
      </Form.Item>
      {/* <Form.Item name="aas" label="Algorithm's Application Score" rules={[{ required: true }]}>
        <InputNumber min={1} max={10} />
      </Form.Item>
      <Form.Item name="difficulty_score" label="Difficulty Score" rules={[{ required: true }]}>
        <InputNumber min={1} max={10} />
      </Form.Item> */}
      <Form.Item label="Custom Solution">
        <CodeEditor code={code} setCode={setCode} />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
      </Form.Item>
    </Form>
  );
};

export default QuestionSubmission;
