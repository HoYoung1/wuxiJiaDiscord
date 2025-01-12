const apiUrl = 'https://xlv1pvl5id.execute-api.ap-northeast-2.amazonaws.com/days'; 

// 데이터를 가져와서 화면에 표시
async function fetchDays() {
  try {
    const response = await fetch(apiUrl);
    const days = await response.json();
    displayDays(days);
  } catch (error) {
    console.error('데이터를 가져오는 데 실패했습니다:', error);
  }
}

// 데이터를 화면에 출력
function displayDays(days) {
  // displayOrder 값에 따라 정렬
  days.sort((a, b) => a.displayOrder - b.displayOrder);

  const daysList = document.getElementById('daysList');
  daysList.innerHTML = ''; // 기존 데이터 지우기

  days.forEach(day => {
    const dayItem = document.createElement('div');
    dayItem.classList.add('day-item');
    dayItem.innerHTML = `
      <strong>${day.dayInKorean}</strong> (${day.ampm})<br>
      시간: ${day.time}<br>
      비고: ${day.comment || '없음'}
    `;
    dayItem.onclick = () => openEditForm(day); // 클릭 시 수정 폼 열기
    daysList.appendChild(dayItem);
  });
}

// 수정 폼 열기
function openEditForm(day) {
  const form = document.getElementById('editForm');
  form.style.display = 'block';

  document.getElementById('dayInKorean').value = day.dayInKorean;
  document.getElementById('ampm').value = day.ampm;
  document.getElementById('time').value = day.time;
  document.getElementById('comment').value = day.comment;

  // 수정 완료 버튼 클릭 시 업데이트
  document.querySelector('button').onclick = () => updateDay(day);
}

// 수정된 정보를 서버에 PUT 요청으로 보내기
async function updateDay(originalDay) {
  const updatedDay = {
    day: originalDay.day,
    ampm: document.getElementById('ampm').value,
    comment: document.getElementById('comment').value,
    dayInKorean: document.getElementById('dayInKorean').value,
    time: document.getElementById('time').value,
    displayOrder: originalDay.displayOrder
  };

  try {
    const response = await fetch(`${apiUrl}/${originalDay.day}`, {
      method: 'PUT',
    //   headers: {
    //     'Content-Type': 'application/json',
    //   },
      body: JSON.stringify(updatedDay)
    });

    if (response.ok) {
      alert('수정이 완료되었습니다.');
      fetchDays(); // 수정 후 데이터 새로고침
      document.getElementById('editForm').style.display = 'none'; // 폼 닫기
    } else {
      alert('수정에 실패했습니다.');
    }
  } catch (error) {
    console.error('수정 요청 실패:', error);
    alert('수정에 실패했습니다.');
  }
}

// 페이지 로드 시 데이터 가져오기
fetchDays();