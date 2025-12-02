'use client';

import { useState } from 'react';
import { SquiggleBlue, TriangleRed, CirclePurple } from '@/components/Squiggles';

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [files, setFiles] = useState<FileList | null>(null);
  const [loading, setLoading] = useState(false);
  const [videos, setVideos] = useState<string[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!files || files.length !== 4) {
      alert('Please upload exactly 4 images.');
      return;
    }
    setLoading(true);

    try {
      // Mock video generation for demo purposes
      // In production, this would call your backend API deployed elsewhere
      await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate processing

      // Generate mock video URLs
      const mockVideos = [
        'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
        'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4'
      ];

      setVideos(mockVideos);
    } catch (err) {
      console.error(err);
      alert('Error generating videos');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <header style={{ marginBottom: '3rem', position: 'relative' }}>
        <div style={{ position: 'absolute', top: -20, left: -40 }}>
          <SquiggleBlue />
        </div>
        <div className="selection-box" style={{ display: 'inline-block' }}>
          <span className="selection-label">Orion</span>
          <h1 style={{ fontSize: '3rem', fontWeight: 900 }}>Video Avatar Agent</h1>
        </div>
        <div style={{ position: 'absolute', top: 10, right: 100 }}>
          <TriangleRed />
        </div>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
        <section>
          <div className="figma-card">
            <h2 style={{ marginBottom: '1rem' }}>Configuration</h2>
            <form onSubmit={handleSubmit}>
              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Prompt</label>
                <textarea
                  className="figma-input"
                  rows={6}
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Describe the character and script..."
                />
              </div>

              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Source Strips (4 images)</label>
                <input
                  type="file"
                  multiple
                  accept="image/*"
                  className="figma-input"
                  onChange={(e) => setFiles(e.target.files)}
                />
                <p style={{ fontSize: '0.8rem', color: '#666' }}>Select exactly 4 images (view1, view2, view3, view4)</p>
              </div>

              <button type="submit" className="figma-button accent" disabled={loading}>
                {loading ? 'Generating...' : 'Generate Video'}
              </button>
            </form>
          </div>
        </section>

        <section>
          <div className="figma-card" style={{ minHeight: '400px', background: '#F3F4F6' }}>
            <h2 style={{ marginBottom: '1rem' }}>Output</h2>
            {videos.length === 0 && !loading && (
              <div style={{ textAlign: 'center', marginTop: '4rem', opacity: 0.5 }}>
                <CirclePurple />
                <p>Generated videos will appear here</p>
              </div>
            )}
            {loading && (
              <div style={{ textAlign: 'center', marginTop: '4rem' }}>
                <p>Working on it...</p>
              </div>
            )}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {videos.map((url, idx) => (
                <div key={idx} className="figma-card">
                  <h3>Scene {idx + 1}</h3>
                  <video src={url} controls style={{ width: '100%', marginTop: '0.5rem' }} />
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
