import React from 'react';
import { Form, Input, Select, Button, InputNumber } from 'antd';

const { Option } = Select;

const FilterForm = ({ onFilter }) => {
  const [form] = Form.useForm();

  const onFinish = (values) => {
    onFilter(values);
  };

  return (
    <Form form={form} layout="inline" onFinish={onFinish}>
      <Form.Item name="text" label="Text">
        <Input placeholder="Search text" />
      </Form.Item>
      <Form.Item name="company" label="Company">
        <Input placeholder="Company" />
      </Form.Item>
      <Form.Item name="difficulty" label="Difficulty">
        <InputNumber min={1} max={10} />
      </Form.Item>
      <Form.Item name="aas" label="AAS">
        <InputNumber min={1} max={10} />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">
          Filter
        </Button>
      </Form.Item>
    </Form>
  );
};

export default FilterForm;
