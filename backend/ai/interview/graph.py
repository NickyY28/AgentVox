"""LangGraph workflow for AgentVox interviews."""

from ai.interview.nodes import (
    analyze_response,
    complete_interview,
    decide_next_action,
    generate_question,
    load_context,
    plan_interview,
    prepare_next_competency,
    select_competency,
)
from ai.interview.state import InterviewState
from langgraph.graph import END, START, StateGraph


def route_after_decision(
    state: InterviewState,
) -> str:
    """Route the workflow after response evaluation."""

    action = state.get(
        "next_action",
    )

    if action == "follow_up":
        return "generate_question"

    if action == "next_competency":
        return "prepare_next_competency"

    return "complete_interview"


def build_interview_graph():
    """Build and compile the interview graph."""

    workflow = StateGraph(
        InterviewState,
    )

    # -------------------------
    # Nodes
    # -------------------------

    workflow.add_node(
        "load_context",
        load_context,
    )

    workflow.add_node(
        "plan_interview",
        plan_interview,
    )

    workflow.add_node(
        "select_competency",
        select_competency,
    )

    workflow.add_node(
        "generate_question",
        generate_question,
    )

    workflow.add_node(
        "analyze_response",
        analyze_response,
    )

    workflow.add_node(
        "decide_next_action",
        decide_next_action,
    )

    workflow.add_node(
        "prepare_next_competency",
        prepare_next_competency,
    )

    workflow.add_node(
        "complete_interview",
        complete_interview,
    )

    # -------------------------
    # Initial flow
    # -------------------------

    workflow.add_edge(
        START,
        "load_context",
    )

    workflow.add_edge(
        "load_context",
        "plan_interview",
    )

    workflow.add_edge(
        "plan_interview",
        "select_competency",
    )

    workflow.add_edge(
        "select_competency",
        "generate_question",
    )

    # -------------------------
    # Response flow
    # -------------------------

    workflow.add_edge(
        "generate_question",
        "analyze_response",
    )

    workflow.add_edge(
        "analyze_response",
        "decide_next_action",
    )

    # -------------------------
    # Adaptive routing
    # -------------------------

    workflow.add_conditional_edges(
        "decide_next_action",
        route_after_decision,
        {
            "generate_question": (
                "generate_question"
            ),
            "prepare_next_competency": (
                "prepare_next_competency"
            ),
            "complete_interview": (
                "complete_interview"
            ),
        },
    )

    workflow.add_edge(
        "prepare_next_competency",
        "select_competency",
    )

    workflow.add_edge(
        "complete_interview",
        END,
    )

    return workflow.compile()


interview_graph = build_interview_graph()
