# ElastiCache_Migration

이 프로젝트는 IDC Redis 서버의 데이터를 AWS ElastiCache로 이관하는 스크립트입니다. 

## 기능

- IDC Redis 서버의 데이터를 AWS ElastiCache로 안전하게 이관합니다.
- Lambda 함수를 사용하여 자동화된 데이터 마이그레이션 수행.

## 사전 조건

- **네트워크 연결**: VPN 또는 Direct Connect(DX)를 통해 AWS VPC와 IDC 간의 연결이 필요합니다.
- **AWS Lambda 설정**: 해당 코드는 AWS Lambda에서 실행되며, Lambda 함수를 VPC 내부에 생성해야 합니다.
- **Redis 라이브러리**: Redis와의 연결을 위해 필요한 라이브러리 구성 필요. 
  - `redis` Python 패키지가 필요합니다.

## 사용 방법

1. **AWS ElastiCache 설정**: ElastiCache 클러스터를 생성하고, 엔드포인트를 확인합니다.
2. **IDC Redis 서버 설정**: IDC Redis 서버에 접근할 수 있는 IP 주소 및 포트 정보 확인합니다.
3. **Lambda 함수 생성**:
   - AWS Lambda 콘솔에서 새로운 Lambda 함수를 생성합니다.
   - 코드를 붙여넣고, 환경 변수에 ElastiCache 엔드포인트 및 IDC Redis 서버 정보를 설정합니다.
   - Lambda 함수의 IAM 역할에 필요한 권한 부여 (VPC 접근 포함).
4. **테스트 실행**: Lambda 함수를 실행하여 데이터 마이그레이션이 정상적으로 작동하는지 확인합니다.

## 코드 설명

- `migration(keys)`: 주어진 키 목록을 사용하여 IDC Redis에서 데이터를 가져와 AWS ElastiCache로 복사합니다. TTL(유효 기간)을 확인하여, TTL이 없는 경우 0으로 설정합니다.
- `lambda_handler(event, context)`: Lambda 함수의 엔트리 포인트로, IDC Redis 서버에서 키를 스캔하고 `migration` 함수를 호출하여 데이터를 이관합니다.
