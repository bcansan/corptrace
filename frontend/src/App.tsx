import React from 'react'
import ReactFlow, { Background } from 'reactflow'
import 'reactflow/dist/style.css'

export const App: React.FC = () => {
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow nodes={[]} edges={[]} fitView>
        <Background />
      </ReactFlow>
    </div>
  )
}
