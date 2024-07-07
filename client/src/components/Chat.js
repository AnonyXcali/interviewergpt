import React, { useState, useEffect, useRef } from 'react';
import { Input, Button, List, message } from 'antd';

const { TextArea } = Input;

const Chat = () => {
  const [query, setQuery] = useState('');
  const [responses, setResponses] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentResponse, setCurrentResponse] = useState('');
  const eventSourceRef = useRef(null);

  const handleSend = async () => {
    if (!query.trim()) {
      message.warning('Please enter a query');
      return;
    }

    setIsLoading(true);
    setCurrentResponse('');
    setResponses((prev) => [...prev, { query, response: '' }]);

    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    eventSourceRef.current = new EventSource(`http://34.132.153.144:5000/stream-query?query=${encodeURIComponent(query)}`);

    eventSourceRef.current.onmessage = (event) => {
      try {
        if (event.data === 'data: [DONE]') {
          eventSourceRef.current.dispatchEvent(new Event('end'));
          return;
        }
        const replaced = event.data.replace('data: ', '');
        const chunk = JSON.parse(replaced);  // Directly parse the JSON string
        if (chunk.choices && chunk.choices[0] && chunk.choices[0].delta && chunk.choices[0].delta.content) {
          setCurrentResponse((prev) => {
            const updatedResponse = prev + chunk.choices[0].delta.content;
            console.log('Updated currentResponse: ', updatedResponse);
            return updatedResponse;
          });
        }
      } catch (error) {
        console.error('Error parsing chunk: ', error);
      }
    };

    eventSourceRef.current.onerror = (error) => {
      console.error('EventSource failed: ', error);
      eventSourceRef.current.close();
      setIsLoading(false);
    };

    eventSourceRef.current.addEventListener('end', () => {
      console.log('Stream ended');
      // setResponses((prev) => {
      //   const updatedResponses = [...prev];
      //   const lastIndex = updatedResponses.length - 1;
      //   if (lastIndex >= 0) {
      //     updatedResponses[lastIndex].response = currentResponse;
      //   }
      //   console.log('Updated responses: ', updatedResponses);
      //   return updatedResponses;
      // });
      setQuery('');
      setCurrentResponse('');
      setIsLoading(false);
      eventSourceRef.current.close();
    });
  };

  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  useEffect(() => {
    if (currentResponse) {
      setResponses((prev) => {
        const lastResponseIndex = prev.length - 1;
        const updatedResponses = [...prev];
        updatedResponses[lastResponseIndex].response = currentResponse;
        return updatedResponses;
      });
    }
  }, [currentResponse]);

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
