from fastapi import APIRouter
from config.db import conn
from sqlalchemy import text


router=APIRouter()



@router.post('/')
async def get_info(item:dict):
    stmt=text("select Usu_Cuenta,Usu_Nombre,Perfil from INDMaeUsuario where Usu_Cuenta='"+item["Usu_Cuenta"]+"' and Usu_Password='"+item["Usu_Password"]+"'")
    users=conn.execute(stmt)
    usersList=users.fetchall()
    return usersList

@router.post('/user/empresas')
async def get_empresas(item:str):
    stmt=("SELECT maeEmpresa.empCodigo, maeEmpresa.empNombre FROM INDUsuNegocio INNER JOIN maeEmpresa ON INDUsuNegocio.CtoEmpresa = maeEmpresa.empCodigo WHERE (INDUsuNegocio.Usu_Cuenta ='"+item+"')group by maeEmpresa.empCodigo, maeEmpresa.empNombre")
    empresas=conn.execute(stmt)
    empresasList=empresas.fetchall()
    return empresasList

@router.post('/user/empresas/obras')
async def get_obras(item:dict):
    stmt=("SELECT INDMaeUNegocioActivas.CtoCodigo,UPPER(INDMaeUNegocioActivas.CtoDescripcion) as Obras FROM INDMaeUNegocioActivas INNER JOIN INDUsuNegocio ON INDMaeUNegocioActivas.CtoCodigo = INDUsuNegocio.CtoCodigo AND INDMaeUNegocioActivas.CtoEmpresa = INDUsuNegocio.CtoEmpresa WHERE (INDUsuNegocio.Usu_Cuenta = '"+item["Usu_Cuenta"]+"') AND (INDUsuNegocio.CtoEmpresa = '"+item["CtoEmpresa"]+"')")
    obras=conn.execute(stmt)
    obrasList=obras.fetchall()
    return obrasList

@router.post('/user/empresas/obras/sector')
async def get_sectores(item:dict):
    stmt=("SELECT DISTINCT Sector FROM INDTrUnidadFisica WHERE (CtoEmpresa = '"+item["CtoEmpresa"]+"') AND (CtoCodigo = '"+item["CtoCodigo"]+"') AND (Sector <> 0)")
    sector=conn.execute(stmt)
    sectorList=sector.fetchall()
    return sectorList

@router.post('/user/empresas/obras/sector/ufisica')
async def get_ufisica(item:dict):
    stmt=("SELECT unidadfisica  FROM INDTrUnidadFisica where CtoEmpresa='"+item["CtoEmpresa"]+"' and CtoCodigo='"+item["CtoCodigo"]+"' and sector='"+item["Sector"]+"' and Sector<>0 ORDER BY unidadfisica ASC")
    uFisica=conn.execute(stmt)
    uFisicaList=uFisica.fetchall()
    return uFisicaList

@router.post('/user/empresas/obras/sector/ufisica/modelo')
async def get_modelo(item:dict):
    stmt=("SELECT [CodMaeVivienda], [UnidadFisica], [Sector], [CtoCodigo], [CtoEmpresa]  FROM [INDTrUnidadFisica]  WHERE ((CtoCodigo = '"+item["CtoCodigo"]+"' AND (Sector = '"+item["Sector"]+"' ) AND (UnidadFisica = '"+item["uFisica"]+"')) and  ctoempresa='"+item["CtoEmpresa"]+"')")
    fila=conn.execute(stmt)
    filaLIst=fila.fetchall()
    return filaLIst

@router.post('/user/cartillacontrol')
async def get_cartilla(item:dict):
    stmt=("SELECT codigo_cartilla, UPPER(descripcion) AS Expr1 FROM indCCalidadCartilla WHERE (codigo_cartilla IN (SELECT DISTINCT codcartilla FROM indCcalidadVB WHERE (ctoempresa = '"+item["CtoEmpresa"]+"') AND (ctocodigo = '"+item["CtoCodigo"]+"') AND (sector = '"+str(item["Sector"])+"' ) AND (uf = '"+item["uFisica"]+"'))) ORDER BY codigo_cartilla")
    cartilla=conn.execute(stmt)
    cartillaList=cartilla.fetchall()
    return cartillaList

@router.post('/user/cartllacontrol/tarifado')
async def get_tarifado(item:dict):
    stmt=("SELECT ISNULL(C.codtarifado, 0) AS codtarifado, ISNULL(UPPER(D.Descripcion), 0) AS TARIFADO FROM indCcalidadVB AS C INNER JOIN INDTrTarifadoDet AS D ON C.ctocodigo = D.CtoCodigo AND C.codtarifado = D.CodTarifadoDet AND C.ctoempresa = D.CtoEmpresa INNER JOIN indCCalidadCartillaActividad AS DD ON C.cartillaact = DD.codigo WHERE (C.ctocodigo = ISNULL('"+str(item["CtoCodigo"])+"', 0)) AND (C.sector = ISNULL('"+str(item["Sector"])+"', 0)) AND (C.uf = ISNULL('"+str(item["uFisica"])+"', 0)) AND (C.codcartilla = ISNULL('"+str(item["Cartilla"])+"', 0)) AND (C.ctoempresa = ISNULL('"+item["CtoEmpresa"]+"', 0)) GROUP BY C.codtarifado, D.Descripcion")
    tarifado=conn.execute(stmt)
    tarifadoList=tarifado.fetchall()
    return tarifadoList

@router.post('/user/cartllacontrol/tarifado/list')
async def get_table(item:dict):
    stmt=("SELECT c.id, isnull(C.ctocodigo,0) as ctoobra, isnull(C.sector,0) as sector, isnull(C.uf,0) as uf,  isnull(C.codcartilla,0) as cartilla, isnull(C.codtarifado,0) as codtarifado, isnull(UPPER(D.Descripcion),0) as TARIFADO, isnull(C.cartillaact,0) as cartillaact, isnull(UPPER(DD.descripcion),0) as ACTIVIDAD, isnull(C.vb,0) as ESTADO, (select  CASE COUNT(*) when 0 THEN case C.vb when 1 then 'APROBADO' when 2 then 'PENDIENTE' when 0 then 'RECHAZADO'  end ELSE 'PAGADO' END   from INDTrActividadxUFisica where ctocodigo=isnull(C.ctocodigo,0) and ctoempresa=isnull(C.ctoempresa,0) and sector=isnull(c.sector,0) and               UnidadFisica=isnull(c.uf,0)   and (CodTipoUF='C' or CodTipoUF='P') AND NumeroTrato<>0  AND CodTarifadoDet=isnull(C.codtarifado,0)  ) as vb1, (select RazonSocial from INDTrContratistas where RutContratista=(select RutContratista from INDEPContratoCAB where IdContrato =  (select IDContrato from INDTrActividadxUFisica where ctoempresa=isnull('"+item["CtoEmpresa"]+"',0) and CtoCodigo=isnull(C.ctocodigo,0) and CodTarifadoDet=isnull(C.codtarifado,0) and Sector=isnull(c.sector,0)  and UnidadFisica=isnull(c.uf,0)))) as Contratista1  FROM          indCcalidadVB C , INDTrTarifadoDet D,indCCalidadCartillaActividad DD WHERE C.CTOCODIGO=D.CTOCODIGO AND C.CODTARIFADO=D.CodTarifadoDet AND   DD.codigo=C.cartillaact and C.ctoempresa=d.CtoEmpresa and C.ctoempresa=isnull('"+item["CtoEmpresa"]+"',0) and C.ctocodigo=isnull('"+item["CtoCodigo"]+"',0) and C.sector=isnull('"+item["Sector"]+"',0) and C.uf=isnull('"+item["uFisica"]+"',0) and C.codcartilla= isnull('"+item["Cartilla"]+"',0) and C.CODTARIFADO= isnull('"+item["Tarifado"]+"',0) order by codtarifado asc, c.id asc")
    informacion=conn.execute(stmt)
    informacionList=informacion.fetchall()
    return informacionList

@router.post('/user/exec')
async def insert_id(item:dict):
    stmt=("INSERT INTO CargaCalidadWebExec (id, usuario, fecha, estado) VALUES ("+item["Id"]+",'"+item["User"]+"',getdate(),'"+item["Estado"]+"')")
    insertid=conn.execute(stmt)
    return "SP Executed"

 