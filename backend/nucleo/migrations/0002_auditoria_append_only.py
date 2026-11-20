"""Torna a trilha de auditoria append-only no próprio banco (RNF-16, HU-045).

Nenhum código da aplicação, nem o admin do Django, nem um SQL manual consegue alterar ou apagar
um registro: o trigger levanta exceção em UPDATE e DELETE.

TRUNCATE não é bloqueado de propósito: o ``flush`` do ``TransactionTestCase`` usa TRUNCATE entre
testes. Em produção, o usuário da aplicação não deve ter privilégio de TRUNCATE (risco documentado
em docs/banco/modelo-dados.md).
"""

from django.db import migrations

CRIAR_TRIGGER = """
CREATE OR REPLACE FUNCTION nucleo_bloquear_alteracao_auditoria() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'RegistroAuditoria é imutável: % não permitido', TG_OP
        USING ERRCODE = 'raise_exception';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER auditoria_sem_update_delete
    BEFORE UPDATE OR DELETE ON nucleo_registroauditoria
    FOR EACH ROW EXECUTE FUNCTION nucleo_bloquear_alteracao_auditoria();
"""

REMOVER_TRIGGER = """
DROP TRIGGER IF EXISTS auditoria_sem_update_delete ON nucleo_registroauditoria;
DROP FUNCTION IF EXISTS nucleo_bloquear_alteracao_auditoria();
"""


class Migration(migrations.Migration):
    dependencies = [("nucleo", "0001_initial")]

    operations = [migrations.RunSQL(CRIAR_TRIGGER, reverse_sql=REMOVER_TRIGGER)]
