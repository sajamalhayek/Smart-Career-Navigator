async function analyzeProfile() {
    const resumeText = document.getElementById('resumeInput').value;
    const targetJob = document.getElementById('jobInput').value;

    if (!resumeText || !targetJob) {
        alert("Please fill in both the resume text and target job description.");
        return;
    }

    document.getElementById('loader').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resume_text: resumeText, target_job: targetJob })
        });

        const data = await response.json();
        document.getElementById('loader').classList.add('hidden');

        if (data.error) {
            alert("Error: " + data.error);
            return;
        }

        document.getElementById('matchScore').innerText = (data.gap_analysis.match_percentage || 0) + "%";
        document.getElementById('readinessLevel').innerText = "Readiness: " + (data.gap_analysis.readiness_level || 'N/A');

        const skillsList = document.getElementById('candidateSkills');
        skillsList.innerHTML = '';
        (data.candidate.technical_skills || []).forEach(skill => {
            const li = document.createElement('li');
            li.innerText = skill;
            skillsList.appendChild(li);
        });

        const missingList = document.getElementById('missingSkills');
        missingList.innerHTML = '';
        (data.gap_analysis.missing_skills || []).forEach(skill => {
            const li = document.createElement('li');
            li.innerText = skill;
            missingList.appendChild(li);
        });

        const roadmapContainer = document.getElementById('roadmapContent');
        roadmapContainer.innerHTML = '';
        (data.roadmap.weekly_plan || []).forEach(item => {
            const div = document.createElement('div');
            div.className = 'week-box';
            div.innerHTML = `
                <h4>Week ${item.week}: ${item.focus_skill}</h4>
                <p><strong>Topics:</strong> ${(item.topics || []).join(', ')}</p>
                <p><strong>Action Item:</strong> ${item.action_item}</p>
            `;
            roadmapContainer.appendChild(div);
        });

        document.getElementById('results').classList.remove('hidden');

    } catch (err) {
        document.getElementById('loader').classList.add('hidden');
        alert("Request failed: " + err);
    }
}