"use client"

import dynamic from 'next/dynamic';
import { FC } from 'react';
import { darkTheme } from 'reagraph';
import { test_file } from './get_concepts';

const GraphCanvas = dynamic(
  () => import('reagraph').then((mod) => mod.GraphCanvas),
  { ssr: false }
);



export const SimpleGraph: FC = () => {

  return (
  <div>
    <button onClick={() => test_file()} className='w-10 bg-amber-200'>Populate</button>
    <div className='h-[300px] bg-black w-full relative'>
      
      <GraphCanvas
        labelType='all'
        theme={darkTheme}
        nodes={[
          {
            id: 'n-1',
            label: '1',
          },
          {
            id: 'n-2',
            label: '2',
          },
        ]}
        edges={[
          {
            id: '1->2',
            source: 'n-1',
            target: 'n-2',
            label: 'Edge 1-2',
          },
        ]}
        
      />
    </div>
  </div>
  );

};