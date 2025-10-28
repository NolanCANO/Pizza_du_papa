from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional

from app.models.size import Size, PizzaSize
from app.models.pizza import Pizza
from app.schemas.size import SizeCreate, SizeUpdate, PizzaSizeCreate, PizzaSizeUpdate


class SizeService:
    """Service pour gérer les tailles de pizza."""
    
    @staticmethod
    def get_all_sizes(db: Session) -> List[Size]:
        """Récupère toutes les tailles."""
        return db.query(Size).all()
    
    @staticmethod
    def get_size_by_id(db: Session, size_id: int) -> Optional[Size]:
        """Récupère une taille par son ID."""
        return db.query(Size).filter(Size.id == size_id).first()
    
    @staticmethod
    def get_size_by_name(db: Session, name: str) -> Optional[Size]:
        """Récupère une taille par son nom."""
        return db.query(Size).filter(Size.name == name).first()
    
    @staticmethod
    def create_size(db: Session, size_data: SizeCreate) -> Size:
        """Crée une nouvelle taille."""
        # Vérifier si le nom existe déjà
        if SizeService.get_size_by_name(db, size_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Une taille avec le nom '{size_data.name}' existe déjà"
            )
        
        size = Size(**size_data.model_dump())
        db.add(size)
        try:
            db.commit()
            db.refresh(size)
            return size
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la création de la taille"
            )
    
    @staticmethod
    def update_size(db: Session, size_id: int, size_data: SizeUpdate) -> Optional[Size]:
        """Met à jour une taille."""
        size = SizeService.get_size_by_id(db, size_id)
        if not size:
            return None
        
        # Vérifier si le nouveau nom existe déjà (si changé)
        if size_data.name and size_data.name != size.name:
            if SizeService.get_size_by_name(db, size_data.name):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Une taille avec le nom '{size_data.name}' existe déjà"
                )
        
        update_data = size_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(size, field, value)
        
        try:
            db.commit()
            db.refresh(size)
            return size
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la mise à jour de la taille"
            )
    
    @staticmethod
    def delete_size(db: Session, size_id: int) -> bool:
        """Supprime une taille."""
        size = SizeService.get_size_by_id(db, size_id)
        if not size:
            return False
        
        # Vérifier s'il y a des pizza_sizes associées
        pizza_sizes_count = db.query(PizzaSize).filter(PizzaSize.size_id == size_id).count()
        if pizza_sizes_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible de supprimer cette taille car elle est utilisée par des pizzas"
            )
        
        db.delete(size)
        db.commit()
        return True


class PizzaSizeService:
    """Service pour gérer les combinaisons pizza-taille."""
    
    @staticmethod
    def get_pizza_sizes_by_pizza(db: Session, pizza_id: int) -> List[PizzaSize]:
        """Récupère toutes les tailles disponibles pour une pizza."""
        return db.query(PizzaSize).filter(PizzaSize.pizza_id == pizza_id).all()
    
    @staticmethod
    def get_pizza_size_by_id(db: Session, pizza_size_id: int) -> Optional[PizzaSize]:
        """Récupère une combinaison pizza-taille par son ID."""
        return db.query(PizzaSize).filter(PizzaSize.id == pizza_size_id).first()
    
    @staticmethod
    def get_pizza_size(db: Session, pizza_id: int, size_id: int) -> Optional[PizzaSize]:
        """Récupère une combinaison pizza-taille spécifique."""
        return db.query(PizzaSize).filter(
            PizzaSize.pizza_id == pizza_id,
            PizzaSize.size_id == size_id
        ).first()
    
    @staticmethod
    def create_pizza_size(db: Session, pizza_size_data: PizzaSizeCreate) -> PizzaSize:
        """Crée une nouvelle combinaison pizza-taille."""
        # Vérifier que la pizza existe
        pizza = db.query(Pizza).filter(Pizza.id == pizza_size_data.pizza_id).first()
        if not pizza:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pizza non trouvée"
            )
        
        # Vérifier que la taille existe
        size = db.query(Size).filter(Size.id == pizza_size_data.size_id).first()
        if not size:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Taille non trouvée"
            )
        
        # Vérifier si la combinaison existe déjà
        existing = PizzaSizeService.get_pizza_size(db, pizza_size_data.pizza_id, pizza_size_data.size_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cette combinaison pizza-taille existe déjà"
            )
        
        pizza_size = PizzaSize(**pizza_size_data.model_dump())
        db.add(pizza_size)
        try:
            db.commit()
            db.refresh(pizza_size)
            return pizza_size
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la création de la combinaison pizza-taille"
            )
    
    @staticmethod
    def update_pizza_size(db: Session, pizza_size_id: int, pizza_size_data: PizzaSizeUpdate) -> Optional[PizzaSize]:
        """Met à jour une combinaison pizza-taille."""
        pizza_size = PizzaSizeService.get_pizza_size_by_id(db, pizza_size_id)
        if not pizza_size:
            return None
        
        update_data = pizza_size_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(pizza_size, field, value)
        
        try:
            db.commit()
            db.refresh(pizza_size)
            return pizza_size
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la mise à jour de la combinaison pizza-taille"
            )
    
    @staticmethod
    def delete_pizza_size(db: Session, pizza_size_id: int) -> bool:
        """Supprime une combinaison pizza-taille."""
        pizza_size = PizzaSizeService.get_pizza_size_by_id(db, pizza_size_id)
        if not pizza_size:
            return False
        
        db.delete(pizza_size)
        db.commit()
        return True
    
    @staticmethod
    def get_price_for_pizza_size(db: Session, pizza_id: int, size_id: int) -> Optional[float]:
        """Calcule le prix pour une combinaison pizza-taille."""
        pizza_size = PizzaSizeService.get_pizza_size(db, pizza_id, size_id)
        if not pizza_size:
            return None
        
        return pizza_size.calculated_price