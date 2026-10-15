import React from 'react';

export const AnalyzerLayout = ({ editorSlot, resultsSlot }) => {
  return (
    <main className="max-w-7xl mx-auto px-4 lg:px-8 py-5 flex-1 w-full">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
        {/* Left Column: Code Editor (7 cols on desktop) */}
        <section className="lg:col-span-7 flex flex-col h-full">
          {editorSlot}
        </section>

        {/* Right Column: Analysis Results (5 cols on desktop) */}
        <section className="lg:col-span-5 flex flex-col h-full">
          {resultsSlot}
        </section>
      </div>
    </main>
  );
};

export default AnalyzerLayout;
