import React, { useState, useRef, useEffect, useCallback } from "react";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';


const ExampleSingleChart = () => {
    const [isPaused, setIsPaused] = useState(false);
    const [data, setData] = useState(null);
    const [gData, setGData] = useState([{
        id: 0, timestamp: 0.00, altitude: 0.00,
        velocity: 0.00, acceleration: 0.00,
        latitude: 0.00, longitude: 0.00,
        temperature: 0.00, pressure: 0.00
    }]);
    const [status, setStatus] = useState("");
    const ws = useRef(null);
    const ws_data = [];


    useEffect(() => {
        if (!isPaused) {
            ws.current = new WebSocket("ws://localhost:8000/api/socket"); // создаем ws соединение
            ws.current.onopen = () => setStatus("Соединение открыто");  // callback на эвент открытия соединения
            ws.current.onclose = () => setStatus("Соединение закрыто"); // callback на эвент закрытия соединения
            gettingData();
        }

        return () => ws.current.close(); // когда меняется isPaused - соединение закрывается
    }, [ws, isPaused]);

    const gettingData = useCallback(() => {
        if (!ws.current) return;

        ws.current.onmessage = e => {                // подписка на получение данных по вебсокету
            if (isPaused) return;
            const message = JSON.parse(e.data);
            setData(JSON.parse(message));
            var msg = JSON.parse(message);
            ws_data.push(JSON.parse(message));
            setGData((prevState)=>[...prevState, JSON.parse(message)]);

        };
    }, [isPaused]);

    return (
        <>
            {!!ws_data &&
                <div>
                    <h2>{status}</h2>
                    {console.log(gData)}
                    <LineChart width={600} height={300} data={gData} margin={{ top: 5, right:20, bottom: 5, left: 5 }}>
                        <Line type="monotone" dataKey="altitude" dot={false} />
                        <CartesianGrid stroke="#ccc" strokeDasharray="3 3"/>
                        <XAxis dataKey="timestamp"/>
                        <YAxis />
                        <Tooltip />
                    </LineChart>

                    <button onClick={() => {
                        ws.current.close();
                        setIsPaused(!isPaused)
                    }}>{!isPaused ? 'Остановить соединение' : 'Открыть соединение' }</button>
                </div>
            }

        </>
    )
}

export default ExampleSingleChart;