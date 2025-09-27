import dataclasses
import sys
from typing import Any, final

import streamlit as st
import openai


@final
@dataclasses.dataclass(frozen=True, slots=True, kw_only=True)
class Message:
    role: Any
    content: Any

    def asdict(self, /) -> Any:
        return {"role": self.role, "content": self.content}


@final
@dataclasses.dataclass(slots=True, kw_only=True)
class SessionState:
    client: openai.OpenAI | None
    messages: list[Message]


SYSTEM_MESSAGE: Message = Message(
    role="system",
    content=(
        "You are a friendly math AI helper that helps school students get "
        "better at math. Expected tasks include explaining solutions to math "
        "problems, solving math problems, and explaining tricky math concepts."
    )
)


DISPLAY_IF: frozenset[str] = frozenset(["user", "assistant"])


TOKEN: str = st.secrets.TOKEN


def session_state() -> SessionState:
    """Gets a `SessionState` instance."""
    if "state" not in st.session_state:
        st.session_state.state = SessionState(
            client=None,
            messages=[SYSTEM_MESSAGE]
        )
    return st.session_state.state


def main() -> None:
    st.title("JVA Math AI 0.1.0")
    state: SessionState = session_state()
    client: openai.OpenAI = openai.OpenAI(api_key=TOKEN)
    for message in state.messages:
        if message.role not in DISPLAY_IF:
            continue
        with st.chat_message(message.role):
            st.markdown(message.content)
    if prompt := st.chat_input("What do you want help with?"):
        st.write(str(state))
        state.messages.append(Message(role="user", content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response = st.write_stream(client.chat.completions.create(
                model="gpt-4",
                messages=[m.asdict() for m in state.messages],
                stream=True,
            ))
        state.messages.append(Message(role="assistant", content=response))


if __name__ == "__main__":
    main()
