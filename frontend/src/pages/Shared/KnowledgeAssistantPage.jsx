import React, { useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import apiClient from "../../services/apiClient";
import { Send, Bot, User, BookOpen } from "lucide-react";

function KnowledgeAssistantPage() {
    const [messages, setMessages] = useState([
        { role: "assistant", content: "Hello! I am your FitNova Knowledge Assistant. Ask me anything about policies, plans, billing, or operations." }
    ]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMessage = input;
        setInput("");
        setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
        setLoading(true);

        try {
            const response = await apiClient.post("/knowledge/chat", { question: userMessage });
            const { answer, sources } = response.data;

            setMessages((prev) => [
                ...prev,
                { role: "assistant", content: answer, sources }
            ]);
        } catch (err) {
            setMessages((prev) => [
                ...prev,
                { role: "assistant", content: "Sorry, I encountered an error. Please try again later." }
            ]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <DashboardLayout>
            <div className="flex flex-col h-[calc(100vh-120px)] max-w-4xl mx-auto bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
                {/* Header */}
                <div className="px-6 py-4 bg-[var(--color-sidebar)] border-b border-gray-200 flex items-center gap-3">
                    <div className="p-2 bg-[var(--color-primary-light)] text-[var(--color-primary)] rounded-lg">
                        <Bot size={20} />
                    </div>
                    <div>
                        <h1 className="font-semibold text-gray-800">FitNova Knowledge Assistant</h1>
                        <p className="text-xs text-gray-500">Retrieves policies, SOPs, and billing rules</p>
                    </div>
                </div>

                {/* Chat window */}
                <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
                    {messages.map((msg, idx) => (
                        <div key={idx} className={`flex gap-3 max-w-2xl ${msg.role === "user" ? "ml-auto flex-row-reverse" : ""}`}>
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 text-white ${msg.role === "user" ? "bg-[var(--color-primary)]" : "bg-gray-400"
                                }`}>
                                {msg.role === "user" ? <User size={16} /> : <Bot size={16} />}
                            </div>
                            <div className={`p-4 rounded-xl ${msg.role === "user" ? "bg-[var(--color-primary)] text-white" : "bg-white border border-gray-200 text-gray-800 shadow-sm"
                                }`}>
                                <p className="text-sm whitespace-pre-line">{msg.content}</p>
                            </div>
                        </div>
                    ))}
                    {loading && (
                        <div className="flex gap-3 max-w-2xl">
                            <div className="w-8 h-8 rounded-full bg-gray-400 flex items-center justify-center text-white">
                                <Bot size={16} />
                            </div>
                            <div className="p-4 bg-white border border-gray-200 rounded-xl flex items-center gap-2">
                                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.4s]"></span>
                            </div>
                        </div>
                    )}
                </div>

                {/* Input area */}
                <form onSubmit={handleSend} className="p-4 border-t border-gray-200 bg-white flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask a question about policies, refunds, or guidelines..."
                        className="flex-1 px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-[var(--color-primary)]"
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        disabled={loading || !input.trim()}
                        className="px-4 py-2.5 bg-[var(--color-primary)] text-white rounded-lg hover:bg-opacity-90 transition-colors disabled:opacity-50 flex items-center justify-center"
                    >
                        <Send size={16} />
                    </button>
                </form>
            </div>
        </DashboardLayout>
    );
}

export default KnowledgeAssistantPage;
