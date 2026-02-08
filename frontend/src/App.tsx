import { CopilotKit, useCoAgent } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export const AgentUI = () => {
  const { state, running, run } = useCoAgent({
    name: "0",   // must match backend agent name
    initialState: {
      messages: [],
      summary_data: null,
      final_count: null,
    },
  });

  return (
    <div style={{ display: "flex", gap: "20px", padding: "20px" }}>
      <div style={{ flex: 1, border: "1px solid #ccc", padding: "20px" }}>
        <h3>Llama Output</h3>
        {running && <p>Processing...</p>}
        {state.summary_data && <p><strong>Summary:</strong> {state.summary_data}</p>}
        {state.final_count && <p><strong>Word Count:</strong> {state.final_count}</p>}
      </div>

      <button onClick={() => run({ state: { input_text: "Test input" } })}>
        Run Agent
      </button>

      <div style={{ width: "400px", height: "600px" }}>
        <CopilotChat
          instructions="Send me text to summarize"
          labels={{
            title: "Llama Summarizer",
            initial: "Hi! Paste some text and I’ll summarize it.",
          }}
        />
      </div>
    </div>
  );
};

export default function App() {
  return (
    <CopilotKit runtimeUrl="http://localhost:8000/copilotkit" agent="0">
        <AgentUI />
    </CopilotKit>
  );
}
