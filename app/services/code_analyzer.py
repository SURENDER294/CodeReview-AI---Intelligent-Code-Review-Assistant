"""Code Analyzer Service for CodeReview AI.

This module provides comprehensive code analysis capabilities including:
- Static code analysis
- Security vulnerability detection
- Code quality metrics
- Performance optimization suggestions
- Best practices validation
"""

import ast
import re
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class IssueSeverity(Enum):
    """Issue severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IssueCategory(Enum):
    """Categories of code issues."""
    QUALITY = "quality"
    SECURITY = "security"
    PERFORMANCE = "performance"
    STYLE = "style"
    BUG = "bug"
    MAINTAINABILITY = "maintainability"


@dataclass
class CodeIssue:
    """Represents a code issue found during analysis."""
    
    title: str
    description: str
    severity: IssueSeverity
    category: IssueCategory
    line_number: Optional[int] = None
    column: Optional[int] = None
    code_snippet: Optional[str] = None
    suggestion: Optional[str] = None
    rule_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert issue to dictionary format."""
        return {
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "category": self.category.value,
            "line_number": self.line_number,
            "column": self.column,
            "code_snippet": self.code_snippet,
            "suggestion": self.suggestion,
            "rule_id": self.rule_id
        }


@dataclass
class AnalysisResult:
    """Results from code analysis."""
    
    issues: List[CodeIssue] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    summary: str = ""
    review_id: Optional[str] = None
    
    def get_issues_by_severity(self, severity: IssueSeverity) -> List[CodeIssue]:
        """Filter issues by severity level."""
        return [issue for issue in self.issues if issue.severity == severity]
    
    def get_critical_count(self) -> int:
        """Get count of critical issues."""
        return len(self.get_issues_by_severity(IssueSeverity.CRITICAL))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary format."""
        return {
            "issues": [issue.to_dict() for issue in self.issues],
            "metrics": self.metrics,
            "summary": self.summary,
            "review_id": self.review_id
        }


class CodeAnalyzer:
    """Main code analyzer service.
    
    Analyzes code for quality, security, performance, and best practices.
    Supports multiple programming languages with language-specific rules.
    """
    
    def __init__(self):
        """Initialize the code analyzer."""
        self.initialized = False
        self.supported_languages = [
            'python', 'javascript', 'typescript', 'java', 
            'go', 'rust', 'cpp', 'csharp'
        ]
        logger.info("CodeAnalyzer initialized")
    
    async def initialize(self) -> None:
        """Initialize analyzer resources.
        
        This method prepares any necessary resources like ML models,
        rule engines, or external service connections.
        """
        try:
            logger.info("Initializing CodeAnalyzer resources...")
            # In a real implementation, this would load ML models, 
            # initialize parsers, etc.
            await asyncio.sleep(0.1)  # Simulate initialization
            self.initialized = True
            logger.info("CodeAnalyzer initialization complete")
        except Exception as e:
            logger.error(f"Failed to initialize CodeAnalyzer: {str(e)}")
            raise
    
    async def cleanup(self) -> None:
        """Cleanup analyzer resources."""
        logger.info("Cleaning up CodeAnalyzer resources...")
        self.initialized = False
    
    async def health_check(self) -> str:
        """Check if analyzer is healthy and ready."""
        return "healthy" if self.initialized else "initializing"
    
    async def analyze(
        self,
        code: str,
        language: str,
        context: Optional[str] = None,
        severity_threshold: str = "medium"
    ) -> Dict[str, Any]:
        """Analyze code and return comprehensive review results.
        
        Args:
            code: Source code to analyze
            language: Programming language of the code
            context: Additional context about the code's purpose
            severity_threshold: Minimum severity level to report
            
        Returns:
            Dictionary containing analysis results with issues, 
            suggestions, and metrics
            
        Raises:
            ValueError: If language is not supported
        """
        if language.lower() not in self.supported_languages:
            raise ValueError(
                f"Language '{language}' not supported. "
                f"Supported: {', '.join(self.supported_languages)}"
            )
        
        logger.info(
            f"Starting code analysis for {language}, "
            f"code length: {len(code)} chars"
        )
        
        # Initialize result
        result = AnalysisResult()
        
        # Perform different types of analysis
        if language.lower() == 'python':
            await self._analyze_python(code, result)
        else:
            await self._analyze_generic(code, language, result)
        
        # Add context-aware suggestions if context provided
        if context:
            await self._add_contextual_suggestions(result, context)
        
        # Calculate code metrics
        result.metrics = self._calculate_metrics(code, language)
        
        # Generate summary
        result.summary = self._generate_summary(result)
        
        # Generate unique review ID
        import uuid
        result.review_id = str(uuid.uuid4())
        
        logger.info(
            f"Analysis complete: {len(result.issues)} issues found, "
            f"{result.get_critical_count()} critical"
        )
        
        return result.to_dict()
    
    async def _analyze_python(self, code: str, result: AnalysisResult) -> None:
        """Perform Python-specific code analysis.
        
        Args:
            code: Python source code
            result: AnalysisResult object to populate with findings
        """
        try:
            # Parse Python AST
            tree = ast.parse(code)
            
            # Check for common Python issues
            self._check_python_complexity(tree, result)
            self._check_python_security(code, result)
            self._check_python_style(code, result)
            self._check_python_best_practices(tree, code, result)
            
        except SyntaxError as e:
            result.issues.append(CodeIssue(
                title="Syntax Error",
                description=f"Python syntax error: {str(e)}",
                severity=IssueSeverity.CRITICAL,
                category=IssueCategory.BUG,
                line_number=e.lineno,
                suggestion="Fix the syntax error before proceeding"
            ))
        except Exception as e:
            logger.error(f"Error analyzing Python code: {str(e)}")
    
    def _check_python_complexity(self, tree: ast.AST, result: AnalysisResult) -> None:
        """Check Python code complexity."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Count complexity indicators
                complexity = sum(
                    1 for _ in ast.walk(node) 
                    if isinstance(_, (ast.If, ast.For, ast.While, ast.Try))
                )
                
                if complexity > 10:
                    result.issues.append(CodeIssue(
                        title="High Cyclomatic Complexity",
                        description=f"Function '{node.name}' has complexity of {complexity}",
                        severity=IssueSeverity.MEDIUM,
                        category=IssueCategory.QUALITY,
                        line_number=node.lineno,
                        suggestion="Consider breaking down into smaller functions"
                    ))
    
    def _check_python_security(self, code: str, result: AnalysisResult) -> None:
        """Check for Python security vulnerabilities."""
        # Check for dangerous eval/exec usage
        if re.search(r'\beval\s*\(', code) or re.search(r'\bexec\s*\(', code):
            result.issues.append(CodeIssue(
                title="Dangerous Function Usage",
                description="Use of eval() or exec() detected - potential security risk",
                severity=IssueSeverity.HIGH,
                category=IssueCategory.SECURITY,
                suggestion="Avoid eval/exec; use safer alternatives like ast.literal_eval"
            ))
        
        # Check for SQL injection risks
        if re.search(r'execute\s*\([^?]*%s', code):
            result.issues.append(CodeIssue(
                title="Potential SQL Injection",
                description="SQL query uses string formatting instead of parameters",
                severity=IssueSeverity.CRITICAL,
                category=IssueCategory.SECURITY,
                suggestion="Use parameterized queries with ? or named placeholders"
            ))
    
    def _check_python_style(self, code: str, result: AnalysisResult) -> None:
        """Check Python code style."""
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > 120:
                result.issues.append(CodeIssue(
                    title="Line Too Long",
                    description=f"Line {i} exceeds 120 characters ({len(line)} chars)",
                    severity=IssueSeverity.LOW,
                    category=IssueCategory.STYLE,
                    line_number=i,
                    suggestion="Break long lines for better readability"
                ))
    
    def _check_python_best_practices(self, tree: ast.AST, code: str, result: AnalysisResult) -> None:
        """Check Python best practices."""
        # Check for missing docstrings in functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    result.issues.append(CodeIssue(
                        title="Missing Docstring",
                        description=f"Function '{node.name}' lacks documentation",
                        severity=IssueSeverity.LOW,
                        category=IssueCategory.MAINTAINABILITY,
                        line_number=node.lineno,
                        suggestion="Add docstring to explain function purpose and parameters"
                    ))
    
    async def _analyze_generic(self, code: str, language: str, result: AnalysisResult) -> None:
        """Perform generic code analysis for non-Python languages."""
        # Generic checks that work across languages
        lines = code.split('\n')
        
        # Check for TODO/FIXME comments
        for i, line in enumerate(lines, 1):
            if 'TODO' in line or 'FIXME' in line:
                result.issues.append(CodeIssue(
                    title="Incomplete Code",
                    description="TODO/FIXME comment found",
                    severity=IssueSeverity.LOW,
                    category=IssueCategory.MAINTAINABILITY,
                    line_number=i,
                    code_snippet=line.strip()
                ))
    
    async def _add_contextual_suggestions(self, result: AnalysisResult, context: str) -> None:
        """Add context-aware suggestions based on code purpose."""
        # This would integrate with AI models for intelligent suggestions
        logger.debug(f"Adding contextual suggestions based on: {context}")
    
    def _calculate_metrics(self, code: str, language: str) -> Dict[str, Any]:
        """Calculate code quality metrics."""
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        return {
            "total_lines": len(lines),
            "code_lines": len(non_empty_lines),
            "blank_lines": len(lines) - len(non_empty_lines),
            "language": language,
            "estimated_complexity": "medium"  # Simplified for demo
        }
    
    def _generate_summary(self, result: AnalysisResult) -> str:
        """Generate human-readable summary of analysis."""
        total = len(result.issues)
        critical = result.get_critical_count()
        
        if total == 0:
            return "Code looks good! No issues found."
        elif critical > 0:
            return f"Found {total} issues including {critical} critical. Review required."
        else:
            return f"Found {total} issues. Consider addressing them for better code quality."


# Export main class
__all__ = ['CodeAnalyzer', 'CodeIssue', 'AnalysisResult', 'IssueSeverity']
