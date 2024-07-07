import React, { useState, useEffect } from 'react';
import { Input, Button, List, message } from 'antd';
import axios from 'axios';

const { TextArea } = Input;

const Chat = () => {
  const [query, setQuery] = useState('');
  const [responses, setResponses] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentResponse, setCurrentResponse] = useState('');

  useEffect(() => {
    if (isLoading) {
      const eventSource = new EventSource('http://34.132.153.144:5000/query');

      eventSource.onmessage = (event) => {
        setCurrentResponse((prev) => prev + event.data);
      };

      eventSource.onerror = (error) => {
        console.error('EventSource failed:', error);
        eventSource.close();
        setIsLoading(false);
      };

      eventSource.addEventListener('end', () => {
        setResponses((prev) => [...prev, { query, response: currentResponse }]);
        setQuery('');
        setCurrentResponse('');
        setIsLoading(false);
        eventSource.close();
      });

      return () => {
        eventSource.close();
      };
    }
  }, [isLoading, query, currentResponse]);

  const handleSend = async () => {
    if (!query.trim()) {
      message.warning('Please enter a query');
      return;
    }

    setIsLoading(true);

    try {
      await axios.post('http://34.132.153.144:5000/query', { prompt: query });
    } catch (error) {
      console.error('Error sending query', error);
      setIsLoading(false);
    }
  };

  return (
    <div>
      <TextArea
        rows={4}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Type your query here"
        disabled={isLoading}
      />
      <Button type="primary" onClick={handleSend} disabled={isLoading}>
        Send
      </Button>
      <List
        itemLayout="horizontal"
        dataSource={responses}
        renderItem={(item) => (
          <List.Item>
            <List.Item.Meta title={item.query} description={item.response} />
          </List.Item>
        )}
      />
    </div>
  );
};

export default Chat;
