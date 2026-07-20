"use client"

import dynamic from 'next/dynamic';
import { FC } from 'react';
import { darkTheme } from 'reagraph';
import concepts from "../../public/data.json"

const GraphCanvas = dynamic(
  () => import('reagraph').then((mod) => mod.GraphCanvas),
  { ssr: false }
);



export const SimpleGraph: FC = () => {


  return (
    <div>
      <div className='h-[300px] bg-black w-full relative'>
        
        <GraphCanvas
          labelType='all'
          theme={darkTheme}
          nodes={concepts.nodes}
          edges={concepts.links}
          
        />
      </div>
    </div>
  );

};