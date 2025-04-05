// File: App.jsx
import { useState } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import { Loader2 } from 'lucide-react';

export default function App() {
  const [view, setView] = useState('home');
  return (
    <main className="min-h-screen bg-gray-50 p-4">
      <h1 className="text-3xl font-bold text-center mb-6">⚖️ AI Legal Assistant</h1>
      <div className="flex justify-center gap-4 mb-8">
        <button onClick={() => setView('chat')} className="btn">Chatbot</button>
        <button onClick={() => setView('doc')} className="btn">Generate Document</button>
        <button onClick={() => setView('rag')} className="btn">Ask a Document</button>
      </div>
      {view === 'chat' && <ChatView />}
      {view === 'doc' && <DocumentView />}
      {view === 'rag' && <RagView />}
    </main>
  );
}

function ChatView() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    setLoading(true);
    const res = await axios.post('http://localhost:8000/chat', new URLSearchParams({ message }));
    setResponse(res.data.response);
    setLoading(false);
  };

  return (
    <motion.div className="max-w-xl mx-auto space-y-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <textarea
        className="w-full border p-2 rounded"
        placeholder="Ask a legal question..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={sendMessage} className="btn">Ask</button>
      {loading && <Loader2 className="animate-spin" />}
      {response && (
        <motion.div className="p-4 bg-white rounded shadow" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <strong>Bot:</strong> {response}
        </motion.div>
      )}
    </motion.div>
  );
}

function DocumentView() {
  const [partyA, setPartyA] = useState('');
  const [partyB, setPartyB] = useState('');
  const [docType, setDocType] = useState('NDA');
  const [result, setResult] = useState('');

  const generate = async () => {
    const res = await axios.post('http://localhost:8000/generate-doc', new URLSearchParams({
      partyA, partyB, doc_type: docType
    }));
    setResult(res.data.document);
  };

  return (
    <motion.div className="max-w-xl mx-auto space-y-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <input type="text" placeholder="Party A" className="input" value={partyA} onChange={(e) => setPartyA(e.target.value)} />
      <input type="text" placeholder="Party B" className="input" value={partyB} onChange={(e) => setPartyB(e.target.value)} />
      <select className="input" value={docType} onChange={(e) => setDocType(e.target.value)}>
        <option value="NDA">NDA</option>
        <option value="Rental Agreement">Rental Agreement</option>
      </select>
      <button onClick={generate} className="btn">Generate</button>
      {result && <motion.div className="bg-white p-4 rounded shadow" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{result}</motion.div>}
    </motion.div>
  );
}

function RagView() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleQuery = async () => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('question', question);
    setLoading(true);
    const res = await axios.post('http://localhost:8000/rag-query', formData);
    setAnswer(res.data.answer);
    setLoading(false);
  };

  return (
    <motion.div className="max-w-xl mx-auto space-y-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} className="input" />
      <textarea
        className="w-full border p-2 rounded"
        placeholder="Ask something from the document..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={handleQuery} className="btn">Submit</button>
      {loading && <Loader2 className="animate-spin" />}
      {answer && <motion.div className="bg-white p-4 rounded shadow" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{answer}</motion.div>}
    </motion.div>
  );
}

