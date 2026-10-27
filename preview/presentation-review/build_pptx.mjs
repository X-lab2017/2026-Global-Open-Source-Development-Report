// Local fallback: the complete deck exceeds the online Pages node limit.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {addSlides} from './native_slides.mjs';
const nodeModules=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
const {Presentation,PresentationFile}=await import(pathToFileURL(path.join(nodeModules,'@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const out=process.argv[2];
process.env.GOSD_DECK_JSON=path.join(out,'deck.json');
const p=Presentation.create({slideSize:{width:1280,height:720}});p.slides.add();
await addSlides(p,0,36,path.join(out,'disc.png'));
// Cover typography has extra breathing room in PowerPoint's font metrics.
const cover=p.slides.getItem(0);for(const s of cover.shapes.items){if(String(s.text)==='Global Open Source Development Report')s.position={...s.position,top:442};}
await fs.mkdir(path.join(out,'native-qa'),{recursive:true});
for(let i=0;i<36;i++){
 const blob=await p.slides.getItem(i).export({format:'png',scale:1});
 await fs.writeFile(path.join(out,'native-qa',`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await blob.arrayBuffer()));
}
const workspace=path.dirname(out);const staging=path.join(workspace,'.native-build');await fs.mkdir(staging,{recursive:true});const candidate=path.join(staging,'candidate-v2.pptx');await(await PresentationFile.exportPptx(p)).save(candidate);
const skillDir='/root/.codex/skills/builtins/presentations';
const {finalizePresentation}=await import(pathToFileURL(path.join(skillDir,'container_tools/artifact_tool_utils.mjs')).href);
const r=await finalizePresentation({workspaceDir:workspace,candidatePath:candidate,finalPath:path.join(out,'GOSD-2026-Opening-Chapter1-Review-v2.pptx'),pythonExecutable:process.env.CODEX_PRIMARY_RUNTIME_PYTHON||'python3',integrityValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],requiredNativeChartOwnerSlides:[11,12,13],requiredNativeTableOwnerSlides:[],materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:['Noto Sans CJK SC']},verifyArtifactToolImport:true,receiptPath:path.join(staging,'validation-v2.json')});
console.log(JSON.stringify(r));
