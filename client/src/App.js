import React from 'react';
import { Layout, Menu } from 'antd';
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Link,
} from 'react-router-dom';
import Chat from './components/Chat';
import QuestionSubmission from './components/QuestionSubmission';
import Dashboard from './components/Dashboard';

const { Header, Content, Footer } = Layout;

const App = () => {
  return (
    <Router>
      <Layout className="layout">
        <Header>
          <div className="logo" />
          <Menu theme="dark" mode="horizontal">
            <Menu.Item key="1">
              <Link to="/">Chat</Link>
            </Menu.Item>
            <Menu.Item key="2">
              <Link to="/submit-question">Submit Question</Link>
            </Menu.Item>
            <Menu.Item key="3">
              <Link to="/dashboard">Dashboard</Link>
            </Menu.Item>
          </Menu>
        </Header>
        <Content style={{ padding: '0 50px' }}>
          <div className="site-layout-content">
            <Routes>
              <Route path="/" element={<Chat />} />
              <Route path="/submit-question" element={<QuestionSubmission />} />
              <Route path="/dashboard" element={<Dashboard />} />
            </Routes>
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>Interview Helper ©2023</Footer>
      </Layout>
    </Router>
  );
};

export default App;
