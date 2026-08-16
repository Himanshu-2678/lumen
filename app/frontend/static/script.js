const API_URL="http://127.0.0.1:8000";
const askInput=document.getElementById("askInput");
const askSend=document.getElementById("askSend");
const evidenceChecks=document.getElementById("evidenceChecks");
const answerBox=document.getElementById("answer");
const answerText=document.getElementById("answerText");
const evidenceSource=document.getElementById("evidenceSource");
const evidenceScore=document.getElementById("evidenceScore");
const closeAnswer=document.getElementById("closeAnswer");
const chips=document.querySelectorAll(".chip");
const kbModal=document.getElementById("kbModal");
const openKb=document.getElementById("openKb");
const closeKb=document.getElementById("closeKb");
const kbBackdrop=document.getElementById("kbBackdrop");
const docList=document.getElementById("docList");
const dropzone=document.getElementById("dropzone");
const fileInput=document.getElementById("fileInput");
const attachButton=document.getElementById("attachButton");
const importButton=document.getElementById("importButton");
const toast=document.getElementById("toast");
const chipsContainer = document.getElementById("chips");
let documents=[];

function showToast(message,type="success"){
    if(!toast)return;
    toast.textContent=message;
    toast.className=`toast show ${type}`;
    setTimeout(()=>{
        toast.className="toast";
    },3000);
}

function autoGrow(){
    askInput.style.height="auto";
    askInput.style.height=Math.min(askInput.scrollHeight,140)+"px";
}

askInput.addEventListener("input",autoGrow);

function delay(ms){
    return new Promise(resolve=>setTimeout(resolve,ms));
}

function renderEvidenceChecks(signals){
    evidenceChecks.innerHTML="";
    if(!signals)return;

    const checks=[];

    if(signals.top_reranker_score>0){
        checks.push("Relevant passage found");
    }

    if(signals.supporting_chunks>1){
        checks.push("Multiple supporting chunks");
    }

    if(signals.metadata_verified){
        checks.push("Source metadata verified");
    }

    if(signals.citation_available){
        checks.push("Citation available");
    }

    checks.forEach(item=>{
        const li=document.createElement("li");
        li.innerHTML=`<span class="check"></span>${item}`;
        evidenceChecks.appendChild(li);
    });
}

async function submitQuestion(){
    const question=askInput.value.trim();

    if(!question){
        askInput.focus();
        return;
    }
    document.getElementById("chips").style.display = "none";
    answerBox.hidden=false;

    answerText.innerHTML=`<span class="thinking">Searching knowledge base<span class="dots"></span></span>`;
    evidenceScore.textContent="...";
    evidenceChecks.innerHTML="";

    evidenceSource.querySelector(".evidence__doc").textContent="Searching sources...";
    evidenceSource.querySelector(".evidence__page").textContent="";

    try{
        await delay(800);

        answerText.innerHTML=`<span class="thinking">Finding relevant evidence<span class="dots"></span></span>`;

        await delay(900);

        answerText.innerHTML=`<span class="thinking">Generating answer<span class="dots"></span></span>`;

        const response=await fetch(`${API_URL}/query/`,{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({question})
        });

        if(!response.ok){
            throw new Error("Query failed");
        }

        const data=await response.json();

        answerText.textContent=data.answer||"No answer found.";

        if(data.confidence){
            const score=Math.round(data.confidence.confidence_score*100);
            evidenceScore.textContent=`${score}%`;
            renderEvidenceChecks(data.confidence.signals);
        }

        if(data.sources && data.sources.length){

            const source = data.sources[0];

            evidenceSource.querySelector(".evidence__doc").textContent =
                source.filename;

            evidenceSource.querySelector(".evidence__page").textContent =
                `Page ${source.page_number}`;

        }
        else{

            evidenceSource.querySelector(".evidence__doc").textContent =
                "No supporting document found";

            evidenceSource.querySelector(".evidence__page").textContent =
                "";
        }
    }
    catch(error){
        console.error(error);
        answerText.textContent="Unable to generate answer.";
        evidenceScore.textContent="—";
        evidenceChecks.innerHTML="";
    }

    answerBox.scrollIntoView({
        behavior:"smooth",
        block:"nearest"
    });
}

askSend.addEventListener("click",submitQuestion);

askInput.addEventListener("keydown",event=>{
    if(event.key==="Enter"&&!event.shiftKey){
        event.preventDefault();
        submitQuestion();
    }
});

closeAnswer.addEventListener("click",()=>{
    answerBox.hidden=true;
});

chips.forEach(chip=>{
    chip.addEventListener("click",()=>{
        askInput.value=chip.textContent;
        autoGrow();
        submitQuestion();
    });
});

function getStatusLabel(doc){
    if(doc.status==="processing"){
        return `
            <span class="processing-status">
                <span class="spinner"></span>
                Processing document...
            </span>
        `;
    }

    if(doc.status==="indexed"){
        return `Ready to chat · ${doc.chunk_count} chunks`;
    }

    if(doc.status==="failed"){
        return "Indexing failed";
    }

    return doc.status;
}

async function loadDocuments(){
    try{
        const response=await fetch(`${API_URL}/documents/`);
        documents=await response.json();
        renderDocuments();
    }
    catch(error){
        console.error("Failed loading documents",error);
    }
}

async function pollDocumentStatus(documentId){
    const interval=setInterval(async()=>{
        try{
            const response=await fetch(
                `${API_URL}/documents/${documentId}`
            );

            if(!response.ok){
                return;
            }

            const document=await response.json();

            renderDocuments();

            if(document.status==="indexed"){
                clearInterval(interval);

                showToast(
                    `${document.filename} is ready to chat ✓`
                );

                await loadDocuments();
            }

            if(document.status==="failed"){
                clearInterval(interval);

                showToast(
                    `${document.filename} failed to process`,
                    "error"
                );

                await loadDocuments();
            }
        }
        catch(error){
            console.error("Polling error",error);
            clearInterval(interval);
        }
    },3000);
}


function startStatusPolling(){
    const interval=setInterval(async()=>{
        await loadDocuments();

        const processing=documents.some(doc=>doc.status==="processing");

        if(!processing){
            clearInterval(interval);

            const indexed=documents.some(doc=>doc.status==="indexed");

            if(indexed){
                showToast("Document ready to chat ✓");
            }
        }
    },3000);
}

function docIconSvg(){
    return `<svg width="15" height="15" viewBox="0 0 16 16" fill="none">
        <path d="M4 2h5l3 3v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1Z" stroke="currentColor" stroke-width="1.2"/>
        <path d="M9 2v3h3" stroke="currentColor" stroke-width="1.2"/>
    </svg>`;
}

function renderDocuments(){
    docList.innerHTML="";

    documents.forEach(doc=>{
        const li=document.createElement("li");
        li.className="docrow";

        li.innerHTML=`
            <div class="docrow__left">
                <span class="docrow__icon">${docIconSvg()}</span>
                <div>
                    <span class="docrow__name">${doc.filename}</span>
                    <div class="docrow__meta">
                        <span class="status-dot ${doc.status}"></span>
                        ${getStatusLabel(doc)}
                    </div>
                </div>
            </div>

            <button class="docrow__del" data-id="${doc.id}" type="button">×</button>
        `;

        docList.appendChild(li);
    });
}

async function uploadDocument(file){
    const tempId = "temp_" + Date.now();
    // Immediately show in UI
    documents.unshift({
        id: tempId,
        filename: file.name,
        status: "uploading",
        chunk_count: 0
    });
    renderDocuments();
    const formData = new FormData();
    formData.append(
        "file",
        file
    );
    try{
        showToast(
            `${file.name} uploading...`
        );
        const response = await fetch(
            `${API_URL}/documents/upload`,
            {
                method:"POST",
                body:formData
            }
        );
        if(!response.ok){
            throw new Error("Upload failed");
        }
        const document = await response.json();
        // Remove temporary item
        documents = documents.filter(
            doc => doc.id !== tempId
        );
        await loadDocuments();
        showToast(
            `${file.name} indexing started`
        );
        pollDocumentStatus(document.id);
    }
    catch(error){
        console.error(error);
        documents = documents.filter(
            doc => doc.id !== tempId
        );
        renderDocuments();
        showToast(
            `${file.name} failed`,
            "error"
        );
    }
}

docList.addEventListener("click",async event=>{
    const button=event.target.closest(".docrow__del");

    if(!button)return;

    await fetch(
        `${API_URL}/documents/${button.dataset.id}`,
        {
            method:"DELETE"
        }
    );

    await loadDocuments();
});

fileInput.addEventListener("change",()=>{
    Array.from(fileInput.files).forEach(uploadDocument);
    fileInput.value="";
});

function openModal(){
    kbModal.hidden=false;
    document.body.style.overflow="hidden";
}

function closeModal(){
    kbModal.hidden=true;
    document.body.style.overflow="";
}

openKb.addEventListener("click",openModal);
closeKb.addEventListener("click",closeModal);
kbBackdrop.addEventListener("click",closeModal);

document.addEventListener("keydown",event=>{
    if(event.key==="Escape"&&!kbModal.hidden){
        closeModal();
    }
});

dropzone.addEventListener("drop",event=>{
    event.preventDefault();

    const files=Array.from(
        event.dataTransfer.files||[]
    );

    files.forEach(uploadDocument);
});

if(attachButton){
    attachButton.addEventListener("click",()=>{
        fileInput.click();
    });
}

if(importButton){
    importButton.addEventListener("click",openModal);
}

loadDocuments();