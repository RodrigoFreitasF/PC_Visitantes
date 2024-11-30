from bpmn_python.bpmn_diagram_rep.bpmn_diagram import BpmnDiagram
from bpmn_python.bpmn_diagram_rep.bpmn_process import BpmnProcess
from bpmn_python.bpmn_diagram_rep.bpmn_lane import BpmnLane
from bpmn_python.bpmn_diagram_rep.bpmn_sequence_flow import BpmnSequenceFlow
from bpmn_python.bpmn_diagram_rep.bpmn_event import BpmnEvent
from bpmn_python.bpmn_diagram_rep.bpmn_activity import BpmnActivity
from bpmn_python.bpmn_diagram_rep.bpmn_gateway import BpmnGateway

# Criando o diagrama BPMN
bpmn_diagram = BpmnDiagram()
bpmn_process = BpmnProcess(id="process_1", name="Gestão de Visitantes")
bpmn_diagram.add_process(bpmn_process)

# Definindo as lanes
lane_portaria = BpmnLane(id="lane_portaria", name="Portaria")
lane_departamento = BpmnLane(id="lane_departamento", name="Departamento")
bpmn_process.add_lane(lane_portaria)
bpmn_process.add_lane(lane_departamento)

# --- Adicionando os elementos do diagrama ---

# Eventos de início e fim
start_event = BpmnEvent(id="start_event_1", type="startEvent", name="Início da Visita")
bpmn_process.add_flow_object(start_event)
end_event = BpmnEvent(id="end_event_1", type="endEvent", name="Fim da Visita")
bpmn_process.add_flow_object(end_event)

# Tarefas da Portaria
cadastrar_visitante = BpmnActivity(id="cadastrar_visitante_1", name="Cadastrar Visitante", lane_id=lane_portaria.id)
bpmn_process.add_flow_object(cadastrar_visitante)
verificar_agendamento = BpmnActivity(id="verificar_agendamento_1", name="Verificar Agendamento", lane_id=lane_portaria.id)
bpmn_process.add_flow_object(verificar_agendamento)
emitir_cracha = BpmnActivity(id="emitir_cracha_1", name="Emitir Crachá", lane_id=lane_portaria.id)
bpmn_process.add_flow_object(emitir_cracha)
registrar_entrada = BpmnActivity(id="registrar_entrada_1", name="Registrar Entrada", lane_id=lane_portaria.id)
bpmn_process.add_flow_object(registrar_entrada)
registrar_saida = BpmnActivity(id="registrar_saida_1", name="Registrar Saída", lane_id=lane_portaria.id)
bpmn_process.add_flow_object(registrar_saida)

# Tarefas do Departamento
receber_visitante = BpmnActivity(id="receber_visitante_1", name="Receber Visitante", lane_id=lane_departamento.id)
bpmn_process.add_flow_object(receber_visitante)
autorizar_entrada = BpmnActivity(id="autorizar_entrada_1", name="Autorizar Entrada", lane_id=lane_departamento.id)
bpmn_process.add_flow_object(autorizar_entrada)

# Gateway
gateway_agendamento = BpmnGateway(id="gateway_agendamento_1", name="Agendamento Existe?", type="exclusiveGateway", gateway_direction="Diverging")
bpmn_process.add_flow_object(gateway_agendamento)

# --- Adicionando os fluxos de sequência ---

# Fluxo principal
bpmn_process.add_sequence_flow(BpmnSequenceFlow(start_event.id, cadastrar_visitante.id))
bpmn_process.add_sequence_flow(BpmnSequenceFlow(cadastrar_visitante.id, verificar_agendamento.id))
bpmn_process.add_sequence_flow(BpmnSequenceFlow(verificar_agendamento.id, gateway_agendamento.id))

# Fluxo condicional para agendamento
bpmn_process.add_sequence_flow(BpmnSequenceFlow(gateway_agendamento.id, autorizar_entrada.id, condition_expression="Sim"))
bpmn_process.add_sequence_flow(BpmnSequenceFlow(gateway_agendamento.id, emitir_cracha.id, condition_expression="Não"))

# Fluxo principal (continuação)
bpmn_process.add_sequence_flow(BpmnSequenceFlow(autorizar_entrada.id, emitir_cracha.id))
bpmn_process.add_sequence_flow(BpmnSequenceFlow(emitir_cracha.id, registrar_entrada.id))
bpmn_process.add_sequence_flow(BpmnSequenceFlow(registrar_entrada.id, receber_visitante.id))
bpmn_process.add_sequence_flow(BpmnSequenceFlow(receber_visitante.id, registrar_saida.id))
bpmn_process.add_sequence_flow(BpmnSequenceFlow(registrar_saida.id, end_event.id))

# --- Exportando o diagrama para um arquivo ---
bpmn_diagram.export_xml_file("diagrama_visitantes.bpmn")