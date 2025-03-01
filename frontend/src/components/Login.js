import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // برای ناوبری پس از ورود
import { Button, Container, Form, Row, Col } from "react-bootstrap"; // استفاده از کامپوننت‌های Bootstrap
import API_BASE_URL from "../config"; // ایمپورت کردن API_BASE_URL

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const navigate = useNavigate();

    const handleLogin = () => {
        const data = new URLSearchParams();
        data.append("username", username);
        data.append("password", password);

        axios
            .post(`${API_BASE_URL}token`, data)
            .then((response) => {
                // ذخیره توکن در localStorage
                localStorage.setItem("access_token", response.data.access_token);
                // هدایت به صفحه لاگ‌ها
                navigate("/logs");
            })
            .catch((error) => {
                // نمایش پیغام خطا از سمت بک‌اند (اگر پیامی از سمت سرور بیاد)
                if (error.response && error.response.data && error.response.data.detail) {
                    setErrorMessage(error.response.data.detail);
                } else {
                    setErrorMessage("خطای ناشناخته، لطفاً دوباره تلاش کنید!");
                }
            });
    };

    return (
        <Container className="mt-5">
            <Row className="justify-content-center">
                <Col md={6} lg={4}>
                    <h2 className="text-center mb-4">ورود به سیستم</h2>
                    {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}
                    <Form>
                        <Form.Group controlId="username">
                            <Form.Label>نام کاربری</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="نام کاربری خود را وارد کنید"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                        </Form.Group>
                        <Form.Group controlId="password" className="mt-3">
                            <Form.Label>رمز عبور</Form.Label>
                            <Form.Control
                                type="password"
                                placeholder="رمز عبور خود را وارد کنید"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </Form.Group>
                        <Button
                            variant="primary"
                            className="mt-3 w-100"
                            onClick={handleLogin}
                        >
                            ورود
                        </Button>
                    </Form>
                </Col>
            </Row>
        </Container>
    );
};

export default Login;
