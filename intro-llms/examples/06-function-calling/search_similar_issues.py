ISSUES_DATABASE = [
    {
        "id": "BUG-234",
        "title": "El login falla en Safari iOS 17",
        "description": "Los usuarios no pueden iniciar sesión usando Safari en iOS 17. El botón de login no responde.",
        "status": "resolved",
        "priority": "Urgent",
        "resolved_date": "2024-01-15",
        "resolution": "Se corrigió un problema de compatibilidad de JavaScript específico de Safari"
    },
    {
        "id": "BUG-156",
        "title": "Timeout del login SSO después de 30 segundos",
        "description": "El login SSO empresarial expira para usuarios con conexiones lentas",
        "status": "open",
        "priority": "High",
        "assigned_to": "auth-team"
    },
    {
        "id": "BUG-089",
        "title": "Email de restablecimiento de contraseña retrasado más de 10 minutos",
        "description": "Los emails de restablecimiento de contraseña tardan demasiado en llegar",
        "status": "resolved",
        "priority": "Medium",
        "resolved_date": "2024-01-10",
        "resolution": "Se actualizó el proveedor de servicio de email"
    },
    {
        "id": "BUG-312",
        "title": "El checkout falla con tarjetas de crédito internacionales",
        "description": "Las tarjetas de crédito no estadounidenses son rechazadas en el checkout",
        "status": "open",
        "priority": "High",
        "assigned_to": "payments-team"
    },
    {
        "id": "BUG-198",
        "title": "El modo oscuro se reinicia al refrescar la página",
        "description": "La preferencia del usuario para modo oscuro no se persiste",
        "status": "open",
        "priority": "Low",
        "assigned_to": "frontend-team"
    },
    {
        "id": "BUG-445",
        "title": "Safari se congela al subir archivos",
        "description": "Subir archivos mayores a 10MB causa que Safari se congele",
        "status": "open",
        "priority": "Medium",
        "assigned_to": "frontend-team"
    }
]

def search_similar_issues(
    keywords: list[str],
    status_filter: str = "all",
    max_results: int = 5
) -> list[dict]:
    """
    Busca issues similares en la base de datos.
    
    En producción, esto conectaría a Jira, GitHub Issues, Linear, etc.
    """
    results = []
    
    for issue in ISSUES_DATABASE:
        # Buscar keywords en título y descripción
        text_to_search = f"{issue['title']} {issue['description']}".lower()
        
        matches = sum(1 for kw in keywords if kw.lower() in text_to_search)

        if matches <= 0:
            continue
        
        # Aplicar filtro de estado
        if status_filter == "all" or issue["status"] == status_filter:
            results.append({
                "id": issue["id"],
                "title": issue["title"],
                "status": issue["status"],
                "priority": issue["priority"],
                "match_score": matches,
                # Incluir info extra si está resuelta
                **({"resolution": issue.get("resolution")} if issue.get("resolution") else {})
            })
    
    # Ordenar por relevancia (número de matches)
    results.sort(key=lambda x: x["match_score"], reverse=True)
    
    return results[:max_results]