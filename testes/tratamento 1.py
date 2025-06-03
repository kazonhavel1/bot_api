import requests
import json

data = """[
    {
        "id_tickets": 7504,
        "observation": null,
        "grid_date_c": null,
        "grid_hour_c": "",
        "test_new": 1,
        "user_role": "tech",
        "total_count": "1",
        "grid_status": "0",
        "grid_reopened_count": "0",
        "grid_date": "2025-06-02T13:50:38.000Z",
        "dt_cad_request": "2025-06-02T13:50:38.000Z",
        "grid_hour": "10:50",
        "grid_date_f": null,
        "grid_hour_f": "",
        "grid_id": "R7383",
        "namecontract": "Suporte Interno",
        "grid_company": "Patrus Transportes",
        "fk_id_company": 1,
        "grid_user": "Cloves Borges (FISCAL MTZ)",
        "grid_tech_solicitant": "Cloves Borges (FISCAL MTZ)",
        "grid_subject": "Documento Logística (CT-e/RPS) com Divergência",
        "grid_tech_group": "TMS",
        "grid_service_technician": "Anna Paula Gomes da Silva",
        "grid_reason_status": null,
        "grid_priority": 34,
        "fk_id_priority": 34,
        "fk_id_urgency": 26,
        "fk_id_impact": 30,
        "fk_id_complexity": 64,
        "description": "Alto",
        "type_tickets": 4,
        "grid_sla": 3,
        "sla_task": 3,
        "sla": "2025-06-02 14:50:38",
        "sla_time": 3,
        "grid_category": "Benner - TMS",
        "grid_catalog_service": "Gestão de Documentos",
        "grid_catalog_task": "Documento Logística (CT-e/RPS) com Divergência",
        "department": null,
        "channel": null,
        "grid_sla_time": "2025-06-02 14:50:38",
        "time_total": null,
        "dt_up": "2025-06-02T14:08:05.000Z",
        "dt_cad": "2025-06-02T13:50:38.000Z",
        "stop_time": 0,
        "stop_ticket": 0,
        "time_total_request": null,
        "status": "In Progress",
        "grid_waiting": "In Progress",
        "grid_time_spent": "",
        "grid_correlation_display": " ",
        "grid_id_integration": null,
        "real_id": "R7383",
        "vipuser": false,
        "id_integration": null,
        "correlation_id": " ",
        "correlation_display": " ",
        "techsol": "",
        "progress": 0,
        "nametech": "Anna Paula Gomes da Silva",
        "workday_next": {
            "0": {},
            "1": {
                "end": "23:59:00",
                "start": "07:00:00"
            },
            "2": {
                "end": "23:59:00",
                "start": "00:00:00"
            },
            "3": {
                "end": "23:59:00",
                "start": "00:00:00"
            },
            "4": {
                "end": "23:59:00",
                "start": "00:00:00"
            },
            "5": {
                "end": "23:59:00",
                "start": "00:00:00"
            },
            "6": {
                "end": "15:00:00",
                "start": "00:00:00"
            }
        },
        "time_pause_next": 0,
        "dt_broken": null,
        "sla_duration": 240
    }
]"""

txt = json.loads(data)

print(txt[0]['id_tickets'])
print(txt[0]['grid_service_technician'])
print(txt[0]['grid_waiting'])
print(txt[0]['grid_tech_group'])