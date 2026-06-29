"use client"

import { useState, type FC } from "react";
import * as d3 from 'd3'


const generateDataset = () => (
  Array(10).fill(0).map(() => ([
    Math.random() * 80 + 10,
    Math.random() * 35 + 10,
  ]))
)


export const GraphView: FC = () => {
    const [dataset, setDataset] = useState(
    generateDataset()
    )
    setInterval(() => {
        const newDataset = generateDataset()
        setDataset(newDataset)
    }, 2000)
    return (
        <svg viewBox="0 0 100 50">
        {dataset.map(([x, y], i) => (
            <circle
            cx={x}
            cy={y}
            r="3"
            key={i}
            />
        ))}
        </svg>
    )
};