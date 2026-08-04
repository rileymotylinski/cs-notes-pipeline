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
      <div className='h-screen bg-black w-full relative'>
        
        <GraphCanvas
          labelType='all'
          theme={darkTheme}
          nodes={concepts.nodes}
          edges={concepts.links}
          renderNode={({ size, color, opacity, selected, id }) => (
            <group>
              <mesh>
                <torusKnotGeometry attach="geometry" args={[size, 1.25, 50, 8]} />
                <meshBasicMaterial
                  attach="material"
                  color={color}
                  opacity={opacity}
                  transparent
                  onUpdate={() => { 
                    if (selected) {
                      console.log("hello")
                    }
                  }}
                />
              </mesh>
            </group>
          )}
          
        />
      </div>
    </div>
  );

};