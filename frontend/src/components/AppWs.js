import React, { useState, useRef, useEffect, useCallback } from "react";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';



const static_data = [{id: 1, timestamp: 1.23, altitude: 100.23}, 
    {id: 2, timestamp: 1.43, altitude: 120.43}, 
    {id: 3, timestamp: 2.00, altitude: 133.00}];


const AppWs = () => {
    const [isPaused, setIsPaused] = useState(false);
    const [data, setData] = useState(null);
    const [gData, setGData] = useState([{id: 0, timestamp: 0.00, altitude: 0.00}]);
    const [status, setStatus] = useState("");
    const ws = useRef(null);
    const ws_data = [];
    

    useEffect(() => {
        if (!isPaused) {
            ws.current = new WebSocket("ws://localhost:8000/api/socket"); // создаем ws соединение
            ws.current.onopen = () => setStatus("Соединение открыто");  // callback на ивент открытия соединения
            ws.current.onclose = () => setStatus("Соединение закрыто"); // callback на ивент закрытия соединения

            gettingData();
        }

        return () => ws.current.close(); // кода меняется isPaused - соединение закрывается
    }, [ws, isPaused]);

    const gettingData = useCallback(() => {
        if (!ws.current) return;

        ws.current.onmessage = e => {                //подписка на получение данных по вебсокету
            if (isPaused) return;
            const message = JSON.parse(e.data);
            setData(JSON.parse(message));
            var msg = JSON.parse(message);
            // setData(message)
            // console.log(message)

            ws_data.push(JSON.parse(message));
            setGData((prevState)=>[...prevState, JSON.parse(message)]);
            // console.log(JSON.parse(message));
            // console.log(ws_data)
        };
    }, [isPaused]);

    // return (
    //     <>
    //         {!!data &&
    //             <div>
    //                 <div>
    //                     <h2>{status}</h2>
    //                     <p>{`package N: ${data?.id}`}</p>
    //                     <p>{`altitude: ${data?.altitude}`}</p>
    //                     <p>{`timestamp: ${data?.timestamp}`}</p>
    //                     <p>{`твоя мама: потная шлюха`}</p>
    //                 </div>
    //                 <button onClick={() => {
    //                     ws.current.close();
    //                     setIsPaused(!isPaused)
    //                 }}>{!isPaused ? 'Остановить соединение' : 'Открыть соединение' }</button>
    //             </div>
    //         }
    //     </>
    // )
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
            {/* <LineChart width={600} height={300} data={ws_data} margin={{ top: 5, right:20, bottom: 5, left: 5 }}>
                <Line type="monotone" dataKey="altitude"/>
                <CartesianGrid stroke="#ccc" strokeDasharray="5 5"/>
                <XAxis dataKey="timestamp"/>
                <YAxis dataKey="altitude"/>
                <Tooltip />
            </LineChart> */}

            {/* {!!data &&
                <div>{data?.id}</div>
            } */}
        </>
    )
}

export default AppWs;