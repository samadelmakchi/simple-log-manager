import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Table, Alert } from "react-bootstrap";
import { Navigate } from "react-router-dom"; // تغییر این قسمت: وارد کردن Navigate از react-router-dom
import API_BASE_URL from "../config"; // ایمپورت کردن API_BASE_URL

const LogList = () => {
    const [logs, setLogs] = useState([]);
    const [errorMessage, setErrorMessage] = useState("");

    useEffect(() => {
        const fetchLogs = async () => {
            const token = localStorage.getItem("access_token"); // گرفتن توکن از localStorage

            // اگر توکن موجود نباشد، به صفحه ورود هدایت می‌کنیم
            if (!token) {
                setErrorMessage("لطفاً وارد شوید!");
                return;
            }

            try {
                const response = await axios.get(`${API_BASE_URL}logs`, {
                    headers: {
                        Authorization: `Bearer ${token}`, // ارسال توکن در هدر
                    },
                });
                setLogs(response.data); // ذخیره لاگ‌ها
            } catch (error) {
                setErrorMessage("خطا در بارگذاری لاگ‌ها!");
                console.error(error);
            }
        };

        fetchLogs();
    }, []);

    return (
        <Container className="mt-5">
            <h2 className="text-center mb-4">لیست لاگ‌ها</h2>
            {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}

            {/* در صورتی که خطای ورود داریم، کاربر به صفحه ورود هدایت می‌شود */}
            {!localStorage.getItem("access_token") && <Navigate to="/" />}

            <Table striped bordered hover responsive>
                <thead>
                    <tr>
                        <th>Microservice</th>
                        <th>تاریخ و زمان</th>
                        <th>پیام</th>
                        <th>URL</th>
                        <th>ID کاربر</th>
                    </tr>
                </thead>
                <tbody>
                    {logs.length > 0 ? (
                        logs.map((log, index) => (
                            <tr key={index}>
                                <td>{log.microservice}</td>
                                <td>{log.datetime}</td>
                                <td>{log.message}</td>
                                <td>{log.url}</td>
                                <td>{log.idu}</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="5" className="text-center">
                                هیچ لاگی یافت نشد
                            </td>
                        </tr>
                    )}
                </tbody>
            </Table>
        </Container>
    );
};

export default LogList;
