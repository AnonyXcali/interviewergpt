import React, { useState, useEffect, useRef } from 'react';
import { Input, Button, List, message } from 'antd';

const { TextArea } = Input;

const Chat = () => {
  const [query, setQuery] = useState('');
  const [responses, setResponses] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentResponse, setCurrentResponse] = useState('');
  const eventSourceRef = useRef(null);
  const variableRef = useRef([]);


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

    eventSourceRef.current = new EventSource(`http://34.132.153.144:5000/stream-query?prompt=${encodeURIComponent(query)}`);


    // eventSourceRef.current.onmessage = (event) => {
    //   console.log('Received chunk: ', event.data);
    //   setCurrentResponse((prev) => {
    //     const updatedResponse = prev + event.data;
    //     console.log('Updated currentResponse: ', updatedResponse);
    //     return updatedResponse;
    //   });
      
    // };

    eventSourceRef.current.addEventListener("message", event => {
      console.log("log", event.data)
      setCurrentResponse((prev) => {
        const updatedResponse = prev + event.data;
        console.log('Updated currentResponse: ', updatedResponse);
        return updatedResponse;
      });

    })
    

    eventSourceRef.current.onerror = (error) => {
      console.error('EventSource failed: ', error);
      eventSourceRef.current.close();
      setIsLoading(false);
    };

    eventSourceRef.current.addEventListener('end', () => {
      console.log('Stream ended');
      setResponses((prev) => {
        const updatedResponses = prev.map((res, index) => 
          index === prev.length - 1 ? { ...res, response: currentResponse } : res
        );
        console.log('Updated responses: ', updatedResponses);
        return updatedResponses;
      });
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

  console.log('Rendering component with responses:', variableRef);

  useEffect(() => {
    variableRef.current = [...variableRef.current, currentResponse];
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
        dataSource={variableRef.current}
        renderItem={(item) => (
          <List.Item>
            <List.Item.Meta title={item} description={item} />
          </List.Item>
        )}
      />
    </div>
  );
};

export default Chat;
