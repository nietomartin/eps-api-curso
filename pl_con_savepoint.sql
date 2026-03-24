-- Crear el procedimiento con SAVEPOINT
CREATE OR REPLACE PROCEDURE sp_con_savepoint(
  p_doc VARCHAR,
  p_cups VARCHAR,
  INOUT p_resultado TEXT DEFAULT NULL
)
LANGUAGE plpgsql AS $$
DECLARE
  v_id_afil INT;
  v_id_cups INT;
BEGIN
  -- Validar afiliado
  SELECT id_afiliado INTO v_id_afil
  FROM afiliado WHERE documento = p_doc;

  IF NOT FOUND THEN
    p_resultado := 'ERROR: Afiliado no encontrado';
    RETURN;
  END IF;

  -- SAVEPOINT después de validar el afiliado
  SAVEPOINT sp_afiliado_validado;

  -- Validar CUPS
  SELECT id_cups INTO v_id_cups
  FROM cups WHERE codigo = p_cups;

  IF NOT FOUND THEN
    -- Revertir solo desde el savepoint
    ROLLBACK TO SAVEPOINT sp_afiliado_validado;
    p_resultado := 'ERROR: CUPS no existe';
    RETURN;
  END IF;

  -- Insertar autorización
  INSERT INTO autorizacion (
    numero_auto, id_afiliado, id_cups,
    id_medico_sol, id_sede, estado
  ) VALUES (
    'AUTO-TEST-SP', v_id_afil, v_id_cups,
    1, 1, 'APROBADA'
  );

  p_resultado := 'APROBADO';

EXCEPTION WHEN OTHERS THEN
  p_resultado := 'ERROR: ' || SQLERRM;
END;
$$;
